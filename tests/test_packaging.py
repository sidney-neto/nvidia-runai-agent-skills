import importlib.util
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
import yaml
from jsonschema import Draft202012Validator
from test_helpers import ROOT, module, fixture

CATALOG='runai-context-discovery runai-cluster-health runai-mcp-integration runai-quota-capacity-planning runai-projects-departments runai-rbac-access runai-workload-policies runai-scheduling-diagnostics runai-workload-lifecycle runai-tls-oidc runai-gpu-sharing runai-upgrade-readiness kubernetes-gpu-operations nvidia-gpu-operator runai-storage runai-networking runai-observability runai-vllm-serving runai-nim-serving runai-distributed-workloads runai-backup-recovery runai-support-report'.split()

class Packaging(unittest.TestCase):
    def test_frontmatter_names_and_local_links(self):
        paths=sorted((ROOT/'skills').glob('*/SKILL.md'))
        self.assertEqual({p.parent.name for p in paths},set(CATALOG))
        for path in paths:
            with self.subTest(skill=path.parent.name):
                text=path.read_text();self.assertTrue(text.startswith('---\n'))
                meta=yaml.safe_load(text.split('---',2)[1])
                self.assertEqual(meta['name'],path.parent.name)
                self.assertRegex(meta['name'],r'^[a-z0-9]+(?:-[a-z0-9]+)*$')
                self.assertLessEqual(len(meta['name']),64)
                self.assertIsInstance(meta['description'],str);self.assertTrue(20<len(meta['description'])<=1024)
                self.assertFalse(set(meta)-{'name','description','license','compatibility','metadata','allowed-tools'})
                self.assertGreater(len(text.split()),170)
                self.assertLess(len(text.split()),3500)
                for md in path.parent.rglob('*.md'):
                    for target in re.findall(r'\]\(([^)]+)\)',md.read_text()):
                        if '://' in target or target.startswith('#'):continue
                        resolved=(md.parent/target.split('#')[0]).resolve()
                        self.assertTrue(resolved.is_relative_to(path.parent.resolve()),f'external required file: {md}:{target}')
                        self.assertTrue(resolved.exists(),f'broken reference: {md}:{target}')
                self.assertEqual((ROOT/'.agents/skills'/path.parent.name).resolve(),path.parent.resolve())
    def test_json_yaml_syntax_and_schema(self):
        for top in ('skills','examples','tests/fixtures','evals','docs','.github'):
            for path in (ROOT/top).rglob('*'):
                if path.suffix=='.json':json.loads(path.read_text(),parse_constant=lambda s: (_ for _ in ()).throw(ValueError(s)))
                elif path.suffix in ('.yaml','.yml'):yaml.safe_load(path.read_text())
        schema=json.loads((ROOT/'skills/runai-context-discovery/assets/snapshot.schema.json').read_text())
        Draft202012Validator.check_schema(schema)
        for path in (ROOT/'examples').glob('*.snapshot.json'):
            module('runai-context-discovery','snapshot').normalize(json.loads(path.read_text()))
        environment=yaml.safe_load((ROOT/'examples/environment.yaml').read_text())
        self.assertEqual(sum(n['gpus'] for n in environment['nodes']),8)
        self.assertEqual(sum(n['role']=='control-plane' for n in environment['nodes']),1)
        self.assertEqual(environment['ingress']['hostname'],'inference.example.com')
    def test_install_individual_skills_outside_repository(self):
        with tempfile.TemporaryDirectory() as tmp:
            for name in CATALOG:
                result=subprocess.run([sys.executable,str(ROOT/'scripts/install_skill.py'),name,'--destination',tmp],capture_output=True,text=True,timeout=10)
                self.assertEqual(result.returncode,0,result.stderr)
                target=Path(tmp)/name
                self.assertTrue((target/'SKILL.md').exists())
                for script in target.glob('scripts/*.py'):
                    result=subprocess.run([sys.executable,str(script),'--help'],cwd=tmp,capture_output=True,text=True,timeout=10)
                    self.assertEqual(result.returncode,0,result.stderr)
            snapshot=Path(tmp)/'input.json';snapshot.write_text(json.dumps(fixture()))
            result=subprocess.run([sys.executable,str(Path(tmp)/'runai-context-discovery/scripts/snapshot.py'),str(snapshot)],cwd=tmp,capture_output=True,text=True,timeout=10)
            self.assertEqual(result.returncode,0,result.stderr)
            result=subprocess.run([sys.executable,str(ROOT/'scripts/install_skill.py'),CATALOG[0],'--destination',tmp],capture_output=True,text=True,timeout=10)
            self.assertEqual(result.returncode,2)
    def test_ci_has_no_write_permission_or_unpinned_actions(self):
        for path in (ROOT/'.github/workflows').glob('*.yml'):
            workflow=yaml.load(path.read_text(),Loader=yaml.BaseLoader)
            self.assertEqual(workflow['permissions'],{'contents':'read'})
            self.assertNotIn('pull_request_target',workflow['on'])
            for job in workflow['jobs'].values():
                for step in job['steps']:
                    if 'uses' in step:self.assertRegex(step['uses'],r'@[a-f0-9]{40}$')
    def test_profiles_have_separate_evidence_and_sources(self):
        rules=json.loads((ROOT/'skills/runai-upgrade-readiness/references/profiles.json').read_text())
        for record in rules['profiles']+rules['transitions']:
            self.assertEqual(set(record['evidence']),{'documentation','fixture','agent_evaluation','live_test'})
            for source in record.get('sources',[record.get('source')]):
                self.assertTrue(source['url'].startswith('https://'))
                self.assertTrue(source['document_version']);self.assertEqual(source['reviewed_at'],'2026-10-18')
    def test_documented_config_fragments_parse(self):
        import tomllib
        for path in (ROOT/'skills').rglob('*.md'):
            for language,body in re.findall(r'```(json|yaml|toml)\n(.*?)\n```',path.read_text(),re.S):
                with self.subTest(path=path,language=language):
                    if language=='json':json.loads(body)
                    elif language=='yaml':yaml.safe_load(body)
                    else:tomllib.loads(body)
    def test_fraction_review_container_and_units(self):
        x=json.loads((ROOT/'examples/fraction-limit-review.json').read_text())
        self.assertEqual(x['submission_path'],'supported-workload YAML')
        annotations=x['after']['metadata']['annotations']
        names={c['name'] for c in x['after']['spec']['containers']}
        self.assertIn(annotations['gpu-fraction-container-name'],names)
        for key,value in annotations.items():
            if key.startswith('nvidia.com/container.'):
                self.assertIn(key.split('.')[2],names)
                self.assertRegex(value,r'^\d+M$')
        self.assertRegex(annotations['gpu-memory'],r'^\d+$')
        self.assertNotIn('apiVersion',x)
    def test_shell_examples_quote_jsonpath_globs(self):
        lines=[line for path in (ROOT/'skills').rglob('*.md') for line in path.read_text().splitlines() if line.startswith('kubectl ')]
        for line in lines:
            if 'custom-columns=' in line:
                self.assertIn("'custom-columns=",line)
        zsh=shutil.which('zsh')
        if zsh:
            for line in lines:
                result=subprocess.run([zsh,'-f','-c','kubectl() { return 0; }\n'+line],capture_output=True,text=True,timeout=5)
                self.assertEqual(result.returncode,0,result.stderr)
