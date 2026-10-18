#!/usr/bin/env python3
"""Offline validation of a skill directory, ZIP, or release; never extracts or executes code."""
import argparse
import ast
import hashlib
import json
from pathlib import Path, PurePosixPath
import posixpath
import re
import stat
import sys
import tomllib
from urllib.parse import unquote, urlsplit
import zipfile
import zlib

import yaml

PROFILE = 'chatgpt-conservative-v1'
# Repository policy, not documented ChatGPT Workspace Agents service limits.
MAX_ZIP = 25_000_000
MAX_FILE = 10_000_000
MAX_TOTAL = 50_000_000
MAX_FILES = 250
NAME = re.compile(r'[a-z0-9]+(?:-[a-z0-9]+)*\Z')
EXTENSIONS = {'.md', '.txt', '.py', '.json', '.yaml', '.yml', '.toml'}
SECRET = re.compile(
    r'-----BEGIN (?:[A-Z ]+ )?PRIVATE KEY-----|'
    r'\b(?:gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}|AKIA[A-Z0-9]{16})\b|'
    r'\bBearer\s+(?![<${])[A-Za-z0-9._-]{20,}|'
    r'(?i:["\']?(?:client[_-]secret|access[_-]token|password|api[_-]key)["\']?\s*[:=]\s*["\'])[A-Za-z0-9+/=_-]{16,}["\']|'
    r'\b(?:10(?:\.\d{1,3}){3}|192\.168(?:\.\d{1,3}){2}|172\.(?:1[6-9]|2\d|3[01])(?:\.\d{1,3}){2})\b'
)


class Invalid(ValueError):
    """A validation rule failed; messages must not echo file contents."""


class StrictLoader(yaml.SafeLoader):
    def compose_node(self, parent, index):
        if self.check_event(yaml.AliasEvent):
            raise Invalid('yaml-alias: aliases are outside the export profile')
        return super().compose_node(parent, index)

    def construct_mapping(self, node, deep=False):
        mapping = {}
        for key_node, value_node in node.value:
            key = self.construct_object(key_node, deep=deep)
            if not isinstance(key, (str, int, float, bool, type(None))) or key in mapping:
                raise Invalid('yaml-key: duplicate or complex mapping key')
            mapping[key] = self.construct_object(value_node, deep=deep)
        return mapping


def parse_yaml(text, label):
    try:
        return yaml.load(text, Loader=StrictLoader)
    except (yaml.YAMLError, RecursionError) as exc:
        raise Invalid(f'{label}: invalid YAML') from exc


def parse_json(text):
    def pairs(items):
        result = {}
        for key, value in items:
            if key in result:
                raise Invalid('json-key: duplicate object key')
            result[key] = value
        return result
    def constant(_):
        raise Invalid('json-number: nonfinite values are invalid')
    return json.loads(text, object_pairs_hook=pairs, parse_constant=constant)


def frontmatter(data, name):
    text = data.decode('utf-8')
    match = re.match(r'\A---\r?\n(.*?)\r?\n---\r?\n(.*)\Z', text, re.S)
    if not match:
        raise Invalid(f'{name}: frontmatter delimiters missing')
    meta = parse_yaml(match[1], name)
    if not isinstance(meta, dict) or meta.get('name') != name or not NAME.fullmatch(name) or len(name) > 64:
        raise Invalid(f'{name}: invalid or mismatched skill name')
    desc = meta.get('description')
    if not isinstance(desc, str) or not 1 <= len(desc.strip()) <= 1024:
        raise Invalid(f'{name}: description must be nonempty and at most 1024 characters')
    if set(meta) - {'name', 'description', 'license', 'compatibility', 'metadata', 'allowed-tools'}:
        raise Invalid(f'{name}: unreviewed frontmatter field')
    for key in ('license', 'compatibility', 'allowed-tools'):
        if key in meta and (not isinstance(meta[key], str) or not meta[key].strip()):
            raise Invalid(f'{name}: invalid {key}')
    if len(meta.get('compatibility', '')) > 500:
        raise Invalid(f'{name}: compatibility exceeds 500 characters')
    if 'metadata' in meta and (not isinstance(meta['metadata'], dict) or
            any(not isinstance(k, str) or not isinstance(v, str) for k, v in meta['metadata'].items())):
        raise Invalid(f'{name}: metadata must map strings to strings')
    if not match[2].strip():
        raise Invalid(f'{name}: Markdown instructions missing')
    return meta, match[2]


def safe_path(value):
    parts = value.split('/')
    if (not value or len(value) > 240 or any(not re.fullmatch(r'[A-Za-z0-9_.-]+', p) or
            p.startswith('.') or p == '__pycache__' or p.endswith('.') or
            re.fullmatch(r'(?i:con|prn|aux|nul|com[1-9]|lpt[1-9])(?:\..*)?', p) for p in parts)):
        raise Invalid('unsafe-path: absolute, traversal, hidden, cache or nonportable entry')
    path = PurePosixPath(value)
    if any(re.search(r'(?i:kubeconfig|credentials|private[-_]?key|service[-_]?account[-_]?token)', p) for p in parts):
        raise Invalid(f'{value}: private-file name')
    if path.suffix.lower() not in EXTENSIONS and path.name not in {'LICENSE', 'NOTICE'}:
        raise Invalid(f'{value}: file type outside the reviewed text-only profile')
    return path


def read_directory(path, skip_caches=False):
    """Skip only reproducible Python caches; reject symlinks before excluding anything."""
    if path.is_symlink() or not path.is_dir():
        raise Invalid('skill-root: expected a real directory')
    files = {}
    for item in sorted(path.rglob('*')):
        if item.is_symlink():
            raise Invalid('symlink: skill resources must be regular files')
        rel = item.relative_to(path).as_posix()
        if skip_caches and ('__pycache__' in item.relative_to(path).parts or item.suffix == '.pyc'):
            continue
        if item.is_dir():
            continue
        if not item.is_file():
            raise Invalid('special-file: not a regular resource')
        safe_path(rel)
        if item.stat().st_size > MAX_FILE:
            raise Invalid(f'{rel}: file-size limit exceeded')
        with item.open('rb') as stream:
            files[rel] = stream.read(MAX_FILE + 1)
        check_sizes(files)
    return files


def check_sizes(files):
    if len(files) > MAX_FILES or sum(map(len, files.values())) > MAX_TOTAL:
        raise Invalid('package-size: file count or total uncompressed size exceeds local policy')
    if any(len(data) > MAX_FILE for data in files.values()):
        raise Invalid('file-size: individual file exceeds local policy')


def check_reference(source, target, files, root_relative=False):
    target = target.strip('<>')
    parts = urlsplit(target)
    if parts.scheme in {'http', 'https', 'mailto'}:
        return
    if parts.scheme or parts.netloc:
        raise Invalid(f'{source}: external filesystem reference')
    target = unquote(parts.path)
    if not target:
        return
    if target.startswith(('/', '~')) or '\\' in target:
        raise Invalid(f'{source}: absolute resource path')
    resolved = posixpath.normpath(posixpath.join('' if root_relative else posixpath.dirname(source), target))
    if resolved == '..' or resolved.startswith('../'):
        raise Invalid(f'{source}: resource escapes packaged skill')
    if resolved not in files and not any(p.startswith(resolved + '/') for p in files):
        raise Invalid(f'{source}: missing packaged resource {resolved}')


def schema_references(obj, source, files):
    if isinstance(obj, dict):
        if obj.get('kind') in ('Secret', 'Config') or any(k in obj for k in ('client-key-data', 'client-certificate-data')):
            raise Invalid(f'{source}: credential-bearing resource type')
        for key, value in obj.items():
            if key == '$ref' and isinstance(value, str):
                if urlsplit(value).scheme or urlsplit(value).netloc:
                    raise Invalid(f'{source}: remote schema dependency breaks offline packaging')
                check_reference(source, value, files)
            schema_references(value, source, files)
    elif isinstance(obj, list):
        for value in obj:
            schema_references(value, source, files)


def validate_contents(name, files, exported=True):
    check_sizes(files)
    if len({p.casefold() for p in files}) != len(files):
        raise Invalid(f'{name}: case-colliding resources')
    entrypoints = [p for p in files if PurePosixPath(p).name.lower() == 'skill.md']
    if entrypoints != ['SKILL.md']:
        raise Invalid(f'{name}: exactly one root SKILL.md required')
    meta, _ = frontmatter(files['SKILL.md'], name)
    if not any(p in files for p in ('LICENSE', 'LICENSE.md', 'LICENSE.txt')):
        raise Invalid(f'{name}: packaged license missing')
    for path, data in files.items():
        safe_path(path)
        suffix = PurePosixPath(path).suffix.lower()
        text = data.decode('utf-8')
        if '\x00' in text or SECRET.search(text):
            raise Invalid(f'{name}/{path}: credential, private address or binary-content indicator; inspect locally')
        if suffix in {'.yaml', '.yml', '.json'}:
            try:
                obj = parse_json(text) if suffix == '.json' else parse_yaml(text, path)
            except (ValueError, RecursionError) as exc:
                raise Invalid(f'{name}/{path}: invalid structured data') from exc
            schema_references(obj, path, files)
        if suffix == '.toml':
            try:
                tomllib.loads(text)
            except tomllib.TOMLDecodeError as exc:
                raise Invalid(f'{name}/{path}: invalid TOML') from exc
        if suffix == '.md':
            # Explicit links and conventional resource paths; dynamic program paths need review/tests.
            for target in re.findall(r'\]\(\s*(<[^>]+>|[^\s)]+)(?:\s+["\'][^\n]*?["\'])?\s*\)', text):
                check_reference(path, target, files)
            for target in re.findall(r'^\s*\[[^\]]+\]:\s*(\S+)', text, re.M):
                check_reference(path, target, files)
            for target in re.findall(r'`((?:scripts|references|assets|agents)/[\w./-]+|requirements\.txt)`', text):
                check_reference(path, target, files, root_relative=True)
    requirements = files.get('requirements.txt', b'').decode().splitlines()
    dependencies = set()
    for line in requirements:
        if not line.strip() or line.startswith('#'):
            continue
        match = re.fullmatch(r'([A-Za-z0-9_-]+)==[0-9]+(?:\.[0-9]+)*(?:[a-z0-9.-]+)?', line)
        if not match:
            raise Invalid(f'{name}: runtime dependencies must be exact package pins, without URLs or options')
        dependencies.add(match[1].replace('-', '_'))
    for path in files:
        if PurePosixPath(path).suffix.lower() != '.py':
            continue
        try:
            tree = ast.parse(files[path], filename=path)
        except SyntaxError as exc:
            raise Invalid(f'{name}/{path}: invalid Python syntax') from exc
        for node in ast.walk(tree):
            imports = [n.name for n in node.names] if isinstance(node, ast.Import) else (
                [node.module] if isinstance(node, ast.ImportFrom) and node.module else [])
            for imported in imports:
                top = imported.split('.')[0]
                local = f'{posixpath.dirname(path)}/{top}'
                if top not in sys.stdlib_module_names | dependencies and local + '.py' not in files and local + '/__init__.py' not in files:
                    raise Invalid(f'{name}/{path}: undeclared or unpackaged import {top}')
    if exported:
        if 'agents/openai.yaml' not in files:
            raise Invalid(f'{name}: generated OpenAI metadata missing')
        agent = parse_yaml(files['agents/openai.yaml'].decode(), name)
        fields = agent.get('interface') if isinstance(agent, dict) else None
        if isinstance(agent, dict) and set(agent) - {'interface', 'policy', 'dependencies'}:
            raise Invalid(f'{name}: unreviewed OpenAI metadata field')
        if not isinstance(fields, dict) or not all(isinstance(fields.get(k), str) and fields[k].strip()
                for k in ('display_name', 'short_description', 'default_prompt')):
            raise Invalid(f'{name}: invalid OpenAI interface metadata')
        if not 25 <= len(fields['short_description']) <= 64 or '$' + name not in fields['default_prompt']:
            raise Invalid(f'{name}: OpenAI metadata length or invocation mismatch')
        if set(fields) - {'display_name', 'short_description', 'default_prompt', 'icon_small', 'icon_large', 'brand_color'}:
            raise Invalid(f'{name}: unreviewed OpenAI interface field')
        for key in ('icon_small', 'icon_large'):
            if key in fields:
                check_reference('agents/openai.yaml', fields[key], files, root_relative=True)
        if 'policy' in agent and (not isinstance(agent['policy'], dict) or
                set(agent['policy']) != {'allow_implicit_invocation'} or
                type(agent['policy']['allow_implicit_invocation']) is not bool):
            raise Invalid(f'{name}: invalid invocation policy')
        if 'dependencies' in agent:
            deps = agent['dependencies']
            if not isinstance(deps, dict) or set(deps) != {'tools'} or not isinstance(deps['tools'], list):
                raise Invalid(f'{name}: invalid tool dependencies')
            for tool in deps['tools']:
                if (not isinstance(tool, dict) or tool.get('type') != 'mcp' or
                        not isinstance(tool.get('value'), str) or
                        set(tool) - {'type', 'value', 'description', 'transport', 'url'}):
                    raise Invalid(f'{name}: unreviewed tool dependency')
    return meta


def read_zip(path):
    if path.is_symlink() or path.stat().st_size > MAX_ZIP:
        raise Invalid('zip-size: symlink or archive exceeds local policy')
    with path.open('rb') as stream:
        if stream.read(4) != b'PK\x03\x04' or path.stat().st_size < 22:
            raise Invalid('zip-entry: unexpected preamble or empty archive')
        stream.seek(-22, 2)
        if stream.read(4) != b'PK\x05\x06':
            raise Invalid('zip-entry: unexpected trailing data or comments')
    with zipfile.ZipFile(path) as archive:
        if archive.comment:
            raise Invalid('zip-entry: archive comments are outside the export profile')
        infos = archive.infolist()
        if len(infos) > MAX_FILES or sum(i.file_size for i in infos) > MAX_TOTAL:
            raise Invalid('package-size: archive count or uncompressed size exceeds local policy')
        names, files, roots = set(), {}, set()
        for info in infos:
            value = info.filename
            # Do not extract anything, even before path and metadata validation.
            if info.orig_filename != value or info.is_dir():
                raise Invalid('zip-entry: NUL or explicit directory entries are outside this profile')
            safe_path(value)
            parts = value.split('/')
            mode = info.external_attr >> 16
            if len(parts) < 2 or (stat.S_IFMT(mode) not in (0, stat.S_IFREG)):
                raise Invalid('zip-entry: non-regular file or missing skill root')
            if (value.casefold() in names or info.flag_bits & (1 | 32 | 64) or info.extra or info.comment or
                    info.compress_type not in {zipfile.ZIP_STORED, zipfile.ZIP_DEFLATED}):
                raise Invalid('zip-entry: duplicate, encrypted or unsupported compression')
            if info.file_size > MAX_FILE:
                raise Invalid('file-size: ZIP member exceeds local policy')
            roots.add(parts[0]); names.add(value.casefold())
            with archive.open(info) as stream:
                data = stream.read(MAX_FILE + 1)
            if len(data) != info.file_size or len(data) > MAX_FILE:
                raise Invalid('zip-entry: member size mismatch')
            files['/'.join(parts[1:])] = data
        if len(roots) != 1:
            raise Invalid('zip-root: exactly one skill directory required')
    return roots.pop(), files


def validate(path):
    name, files = (path.name, read_directory(path)) if path.is_dir() else read_zip(path)
    meta = validate_contents(name, files)
    return {'skill': name, 'status': 'valid', 'profile': PROFILE, 'files': len(files), 'description': meta['description']}


def verify_release(path):
    if path.is_symlink() or not path.is_dir() or any(p.is_symlink() or not p.is_file() for p in path.iterdir()):
        raise Invalid('release: expected regular files in a real directory')
    for filename in ('manifest.json', 'SHA256SUMS'):
        if (path / filename).stat().st_size > MAX_FILE:
            raise Invalid('manifest: metadata exceeds size policy')
    manifest = parse_json((path / 'manifest.json').read_text())
    if (not isinstance(manifest, dict) or not isinstance(manifest.get('skills'), list) or
            manifest.get('compatibility_profile') != PROFILE or manifest.get('skill_count') != len(manifest['skills'])):
        raise Invalid('manifest: profile or count mismatch')
    if (manifest.get('repository') != 'sidney-neto/nvidia-runai-agent-skills' or
            not re.fullmatch(r'v?\d+\.\d+\.\d+(?:[-+][A-Za-z0-9.-]+)?', manifest.get('release_version', '')) or
            type(manifest.get('source_dirty')) is not bool or
            (manifest.get('git_commit') is not None and not re.fullmatch(r'[a-f0-9]{40}', manifest['git_commit']))):
        raise Invalid('manifest: invalid source metadata')
    checksums = []
    names = set()
    for record in manifest['skills']:
        name = record['name']; filename = record['package']
        if name in names or not NAME.fullmatch(name) or filename != f'nvidia-runai-{name}.zip':
            raise Invalid('manifest: duplicate skill or unsafe asset name')
        names.add(name)
        if not isinstance(record.get('runtime_limitations'), list) or not all(isinstance(v, str) for v in record['runtime_limitations']):
            raise Invalid(f'{name}: runtime limitations missing')
        package = path / filename
        result = validate(package)
        data = package.read_bytes(); digest = hashlib.sha256(data).hexdigest()
        if (result['skill'] != name or result['description'] != record['description'] or
                digest != record['sha256'] or len(data) != record['size_bytes'] or record['validation'] != 'valid'):
            raise Invalid(f'{name}: manifest does not match validated archive')
        checksums.append(f'{digest}  {filename}\n')
    if not names or (path / 'SHA256SUMS').read_text() != ''.join(checksums):
        raise Invalid('checksums: missing, unordered or mismatched SHA256SUMS')
    if {p.name for p in path.iterdir()} != {r['package'] for r in manifest['skills']} | {'manifest.json', 'SHA256SUMS'}:
        raise Invalid('manifest: unexpected or missing release files')
    return {'status': 'valid', 'profile': PROFILE, 'skills': len(names)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('paths', type=Path, nargs='+')
    parser.add_argument('--release', action='store_true', help='validate release manifest, every ZIP and checksums')
    parser.add_argument('--json', action='store_true', help='machine-readable results, including failures')
    args = parser.parse_args(); results = []
    for path in args.paths:
        try:
            results.append((verify_release if args.release else validate)(path))
        except (ValueError, OSError, KeyError, TypeError, zipfile.BadZipFile, zlib.error, RuntimeError, RecursionError) as exc:
            results.append({'status': 'invalid', 'path': path.name,
                            'error': str(exc) if isinstance(exc, Invalid) else 'Unreadable or malformed package; inspect locally.'})
    print(json.dumps(results, indent=2, sort_keys=True) if args.json else '\n'.join(
        f"{r.get('skill', r.get('path', 'release'))}: {r['status']} {r.get('error', '')}" for r in results))
    return int(any(r['status'] != 'valid' for r in results))


if __name__ == '__main__':
    sys.exit(main())
