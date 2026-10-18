import copy
import importlib.util
import json
from pathlib import Path
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
def module(skill, name):
    path = ROOT / 'skills' / skill / 'scripts' / (name + '.py')
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

def fixture():
    return json.loads((ROOT / 'tests/fixtures/eight-gpu.json').read_text())

class Helpers(unittest.TestCase):
    def test_quota_separates_parents_and_unknowns(self):
        q = module('runai-quota-capacity-planning', 'quota')
        report = q.calculate(fixture())
        pool = report['pools'][0]
        self.assertEqual(pool['physical_gpus'], 8)
        self.assertEqual(pool['finite_project_quota'], 12)
        self.assertEqual(pool['finite_department_quota'], 8)
        self.assertTrue(pool['configured_oversubscription'])
        self.assertEqual(pool['over_quota_projects'], ['research'])
        data = fixture(); data['quotas'][0]['quota'] = 'unlimited'; data['quotas'][1]['quota'] = None
        result = q.calculate(data)['pools'][0]
        self.assertEqual(result['unlimited_projects'], ['research'])
        self.assertEqual(result['unknown_projects'], ['serving'])
        self.assertFalse(result['quota_total_complete'])

    def test_unknown_versions_preserved(self):
        s = module('runai-context-discovery', 'snapshot')
        data = fixture(); data['components'][0]['raw_version'] = None
        result = s.normalize(data)
        self.assertEqual(result['components'][0]['version_state'], 'missing')
        self.assertIsNone(result['components'][0]['raw_version'])
        self.assertEqual(s.version('v2.10.0')['parts'], [2,10,0])
        self.assertGreater(s.version('2.10.0')['parts'], s.version('2.9.0')['parts'])
        for raw in ('3.0.0-rc.1','3.0.0-vendor','main','2.x',' 3.0 / 2.26 '):
            self.assertNotEqual(s.version(raw)['state'], 'release')

    def test_offline_no_external_access(self):
        with patch('subprocess.Popen', side_effect=AssertionError('live process')), patch('socket.socket', side_effect=AssertionError('network')), patch('pathlib.Path.home', side_effect=AssertionError('credentials')):
            data = fixture()
            self.assertEqual(module('runai-context-discovery','snapshot').normalize(data)['schema_version'], 1)
            self.assertTrue(module('runai-quota-capacity-planning','quota').calculate(data)['pools'])
            self.assertTrue(module('runai-cluster-health','health').analyze(data)['findings'])

    def test_pending_fragmentation(self):
        m = module('runai-scheduling-diagnostics','fit')
        result = m.analyze(fixture())
        self.assertTrue(result['aggregate_sufficient'])
        self.assertFalse(result['single_device_fit'])
        self.assertIn('fragmentation',result['findings'])

    def test_tls_host_is_not_application(self):
        m = module('runai-tls-oidc','tls_evidence')
        result = m.analyze({'administrator_tls_verified': True,'application_tls_verified': False,'application_error': 'x509: certificate signed by unknown authority'})
        self.assertEqual(result['state'],'application_trust_unverified')

    def test_vllm_memory_budget(self):
        m = module('runai-vllm-serving','budget')
        r = m.analyze({'max_model_len':32768,'max_num_seqs':16,'kv_bytes_per_token_per_gpu':131072,'available_kv_bytes_per_gpu':8589934592})
        self.assertEqual(r['state'],'inconsistent_full_concurrency_budget')
        self.assertEqual(r['full_length_sequence_capacity'],2)

    def test_single_control_plane(self):
        r = module('runai-cluster-health','health').analyze(fixture())
        self.assertIn('single_control_plane_no_ha_assumption',r['findings'])

    def test_snapshot_rejects_secrets_and_bad_units(self):
        s = module('runai-context-discovery','snapshot')
        data = fixture(); data['credentials']={'token':'synthetic-secret'}
        with self.assertRaises(ValueError):s.normalize(data)
        data = fixture(); data['quotas'][0]['quota']=-1
        with self.assertRaises(ValueError):s.normalize(data)

    def test_report_redacts_nested_and_free_text(self):
        m = module('runai-support-report','report')
        raw={'token':'SYNTHETIC_TOKEN','message':'Authorization: Bearer FAKE_TOKEN password=FAKE_PASSWORD https://user:pass@example.com/path?token=FAKE_QUERY','nested':[{'client_secret':'FAKE_SECRET'}], 'log':'-----BEGIN PRIVATE KEY-----\nFAKE_BODY\n-----END PRIVATE KEY-----'}
        text=json.dumps(m.redact(raw))
        for value in ('SYNTHETIC_TOKEN','FAKE_TOKEN','FAKE_PASSWORD','FAKE_QUERY','FAKE_SECRET','FAKE_BODY','user:pass'):
            self.assertNotIn(value,text)

if __name__ == '__main__': unittest.main()

class InputBoundaries(unittest.TestCase):
    def test_tls_boolean_is_not_integer(self):
        m=module('runai-tls-oidc','tls_evidence')
        with self.assertRaises(ValueError):m.analyze({'application_tls_verified':1})
