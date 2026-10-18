#!/usr/bin/env python3
"""Build independent, reproducible skill ZIPs; no network, installs or helper execution."""
import argparse
import hashlib
import io
import json
from pathlib import Path
import re
import stat
import subprocess
import sys
import tomllib
import zipfile

import yaml

from validate_chatgpt_skill import (Invalid, MAX_ZIP, PROFILE, frontmatter,
                                   read_directory, validate_contents, verify_release)

ROOT = Path(__file__).resolve().parents[1]


def discover(root):
    skills = root / 'skills'
    found = []
    for path in sorted(skills.iterdir()):
        if path.is_symlink():
            raise Invalid('discovery: canonical skills cannot be symlinks')
        if path.is_dir():
            if not (path / 'SKILL.md').is_file():
                raise Invalid(f'{path.name}: canonical directory missing SKILL.md')
            found.append(path)
    if not found:
        raise Invalid('discovery: no canonical skills found')
    return found


def agent_metadata(name, body):
    title = re.search(r'^# (.+)$', body, re.M)
    title = title[1].strip() if title and title[1].strip() else name.replace('-', ' ').capitalize()
    short = title if len(title) >= 25 else title + ' from sanitized evidence'
    if len(short) > 64:
        short = short[:64].rsplit(' ', 1)[0]
    display = ' '.join({'runai': 'Run:ai', 'nvidia': 'NVIDIA', 'gpu': 'GPU',
                        'mcp': 'MCP', 'rbac': 'RBAC', 'tls': 'TLS', 'oidc': 'OIDC',
                        'vllm': 'vLLM', 'nim': 'NIM'}.get(w, w.capitalize()) for w in name.split('-'))
    # JSON-quoted scalar strings are also YAML strings; this is stable across PyYAML versions.
    values = {'display_name': display, 'short_description': short,
              'default_prompt': f'Use ${name} to {title[0].lower() + title[1:]} from sanitized evidence; identify versions and gaps without live access.'}
    return ('interface:\n' + ''.join(f'  {k}: {json.dumps(v, ensure_ascii=False)}\n' for k, v in values.items())).encode('utf-8')


def export(path):
    files = read_directory(path, skip_caches=True)
    meta = validate_contents(path.name, files, exported=False)
    _, body = frontmatter(files['SKILL.md'], path.name)
    # Keep supported optional metadata and the entire body, including legal information.
    files['SKILL.md'] = ('---\n' + yaml.safe_dump(meta, sort_keys=False, allow_unicode=True, width=1000) +
                         '---\n' + body).encode('utf-8')
    if 'agents/openai.yaml' not in files:
        files['agents/openai.yaml'] = agent_metadata(path.name, body)
    validate_contents(path.name, files)
    return files, meta


def zip_bytes(name, files):
    buffer = io.BytesIO()
    # Stored text is small here and avoids compression-library-dependent bytes.
    with zipfile.ZipFile(buffer, 'w', compression=zipfile.ZIP_STORED) as archive:
        for path, data in sorted(files.items()):
            info = zipfile.ZipInfo(f'{name}/{path}', date_time=(1980, 1, 1, 0, 0, 0))
            info.create_system = 3
            info.external_attr = (stat.S_IFREG | 0o644) << 16
            archive.writestr(info, data)
    data = buffer.getvalue()
    if len(data) > MAX_ZIP:
        raise Invalid(f'{name}: ZIP exceeds local size policy')
    return data


def build(skills, output, version, commit, dirty=False):
    pending = {}; records = []; sums = []
    for path in sorted(skills):
        files, meta = export(path)
        data = zip_bytes(path.name, files)
        asset = f'nvidia-runai-{path.name}.zip'
        digest = hashlib.sha256(data).hexdigest()
        pending[f'{path.name}/skill.zip'] = data
        pending[f'release/{asset}'] = data
        limitations = ['ChatGPT import and agent execution unverified; no tools or permissions granted.']
        if any(p.endswith('.py') for p in files):
            limitations.append('Optional helpers require Python 3.11+ and permitted code execution; no automatic dependency installation.')
        if 'requirements.txt' in files:
            limitations.append('Runtime pins: ' + ', '.join(files['requirements.txt'].decode().splitlines()))
        records.append({'name': path.name, 'description': meta['description'], 'package': asset,
                        'size_bytes': len(data), 'sha256': digest, 'validation': 'valid',
                        'runtime_limitations': limitations})
        sums.append(f'{digest}  {asset}\n')
    manifest = {'repository': 'sidney-neto/nvidia-runai-agent-skills', 'release_version': version,
                'git_commit': commit, 'source_dirty': dirty, 'compatibility_profile': PROFILE,
                'skill_count': len(records), 'skills': records}
    pending['release/manifest.json'] = (json.dumps(manifest, indent=2, sort_keys=True, ensure_ascii=False) + '\n').encode()
    pending['release/SHA256SUMS'] = ''.join(sums).encode()
    if output.is_symlink() or (output.exists() and not output.is_dir()):
        raise Invalid('output: expected a real directory')
    # No recursive deletion or silent replacement of a different release or unrelated data.
    existing = list(output.rglob('*')) if output.exists() else []
    if any(p.is_symlink() or (p.is_file() and (p.relative_to(output).as_posix() not in pending or
            p.stat().st_size != len(pending[p.relative_to(output).as_posix()]) or
            p.read_bytes() != pending[p.relative_to(output).as_posix()])) for p in existing):
        raise Invalid('output: contains different files or symlinks; choose a fresh --output directory')
    for relative, data in pending.items():
        target = output / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
    verify_release(output / 'release')
    return manifest


def revision(root):
    try:
        commit = subprocess.run(['git', 'rev-parse', 'HEAD'], cwd=root, capture_output=True,
                                text=True, check=True, timeout=5).stdout.strip()
        dirty = bool(subprocess.run(['git', 'status', '--porcelain'], cwd=root, capture_output=True,
                                   text=True, check=True, timeout=5).stdout.strip())
        return commit, dirty
    except (OSError, subprocess.SubprocessError):
        return None, True


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    choice = parser.add_mutually_exclusive_group(required=True)
    choice.add_argument('--list', action='store_true')
    choice.add_argument('--all', action='store_true')
    choice.add_argument('--skill')
    parser.add_argument('--validate-only', action='store_true')
    parser.add_argument('--output', type=Path, default=ROOT / 'dist/chatgpt')
    parser.add_argument('--version', help='manifest version; defaults to pyproject.toml version')
    parser.add_argument('--json', action='store_true')
    args = parser.parse_args()
    try:
        skills = discover(ROOT)
        if args.skill:
            skills = [p for p in skills if p.name == args.skill]
            if not skills:
                raise Invalid('selection: unknown canonical skill; use --list')
        if args.list:
            result = {'skills': [p.name for p in skills]}
        elif args.validate_only:
            result = {'profile': PROFILE, 'skills': [{'name': p.name, 'status': 'valid',
                      'files': len(export(p)[0])} for p in skills]}
        else:
            version = args.version or tomllib.loads((ROOT / 'pyproject.toml').read_text())['project']['version']
            if not re.fullmatch(r'v?\d+\.\d+\.\d+(?:[-+][A-Za-z0-9.-]+)?', version):
                raise Invalid('version: expected a semantic release version')
            commit, dirty = revision(ROOT)
            result = build(skills, args.output, version, commit, dirty)
        print(json.dumps(result, indent=2, sort_keys=True) if args.json else
              '\n'.join(p.name for p in skills) + f'\n{len(skills)} skills; ' +
              ('listed' if args.list else 'validated' if args.validate_only else f'packaged in {args.output}'))
        return 0
    except (ValueError, OSError, KeyError, TypeError, RecursionError) as exc:
        message = str(exc) if isinstance(exc, Invalid) else 'Unreadable or malformed skill; inspect locally.'
        if args.json:
            print(json.dumps({'status': 'invalid', 'error': message}, sort_keys=True))
        else:
            print(message, file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
