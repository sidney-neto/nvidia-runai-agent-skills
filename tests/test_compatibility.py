import copy
import json
import unittest
from test_helpers import module, ROOT

class Compatibility(unittest.TestCase):
    def setUp(self):
        self.m=module('runai-upgrade-readiness','readiness')
        self.profiles=json.loads((ROOT/'skills/runai-upgrade-readiness/references/profiles.json').read_text())
    def environment(self, version='3.0'):
        return {'scope':'lab','deployment':'self-hosted','workload_type':'supported-workload YAML','settings':{'fractional GPU workload':True,'observed effective memory limit':True},'components':{'runai-cluster':{'raw_version':version,'origin':'synthetic chart metadata'},'runai-control-plane':{'raw_version':'2.26','origin':'synthetic'},'runai-cli':{'raw_version':'2.25','origin':'synthetic'}},'capabilities':{'fraction-limit':{'state':'available','advertised':True,'usable':True,'permitted':True}}}
    def test_both_families_and_unknown(self):
        old=self.m.select(self.environment('v2.26'),self.profiles,'fraction-limit')
        new=self.m.select(self.environment(),self.profiles,'fraction-limit')
        self.assertEqual(old['profile']['id'],'fractions-226')
        self.assertEqual(new['profile']['id'],'fractions-300')
        self.assertIn('ignored',new['profile']['behavior'])
        for raw in ('9.0','3.0.1','3.0.0-rc.1','3.0.0-vendor',None,'main'):
            self.assertEqual(self.m.select(self.environment(raw),self.profiles,'fraction-limit')['state'],'missing-evidence')
    def test_capability_states_are_not_permissions(self):
        for state in ('absent','deprecated','removed','experimental','disabled','unavailable','permission-denied','unverified','vendor-unsupported'):
            env=self.environment();env['capabilities']['fraction-limit']['state']=state
            self.assertEqual(self.m.select(env,self.profiles,'fraction-limit')['state'],state)
        env=self.environment();env['capabilities']['fraction-limit']['permitted']=False
        self.assertEqual(self.m.select(env,self.profiles,'fraction-limit')['state'],'permission-denied')
        env=self.environment();env['capabilities']['fraction-limit']['usable']=False
        self.assertEqual(self.m.select(env,self.profiles,'fraction-limit')['state'],'unverified')
    def test_conflicts_and_local_claims(self):
        profiles=copy.deepcopy(self.profiles);profiles['profiles'].append(profiles['profiles'][1])
        self.assertEqual(self.m.select(self.environment(),profiles,'fraction-limit')['state'],'conflict')
        env=self.environment();env['local_profile']={'component':'runai-cluster','raw_version':'2.26','provenance':'custom','scope':'lab','captured_at':'2026-10-18T00:00:00Z'}
        self.assertEqual(self.m.select(env,self.profiles,'fraction-limit')['state'],'conflict')
    def test_component_versions_remain_independent(self):
        result=self.m.select(self.environment(),self.profiles,'fraction-limit')
        self.assertEqual(result['observed_component'],'runai-cluster')
        self.assertEqual(result['profile']['id'],'fractions-300')
    def ready(self):
        return {'components':{'runai-control-plane':{'raw_version':'2.26','origin':'synthetic'},'runai-cluster':{'raw_version':'2.26','origin':'synthetic'},'runai-cli':{'raw_version':'2.26','origin':'synthetic'}},'current':'2.26','target':'3.0','deployment':'self-hosted','edition':'support-entitled','kubernetes':'1.35.0','fractions':True,'prerequisites':{key:True for key in ('backups_verified','artifacts_verified','entitlement_verified','persistence_verified','recovery_reviewed','driver_r615_verified','cuda_13_4_verified','gpu_operator_26_7_1_verified','nri_disabled_verified','fraction_manifests_reviewed','sources_refreshed')}}
    def test_documented_component_stages(self):
        r=self.m.plan(self.ready(),self.profiles)
        self.assertEqual(r['state'],'documented-plan')
        self.assertLess(r['stages'].index('control-plane'),r['stages'].index('cluster'))
        data=self.ready();data['prerequisites']['backups_verified']=False
        self.assertEqual(self.m.plan(data,self.profiles)['state'],'missing-prerequisites')
    def test_incompatible_and_unverified_transition(self):
        data=self.ready();data['kubernetes']='1.34.0'
        self.assertEqual(self.m.plan(data,self.profiles)['state'],'incompatible')
        data=self.ready();data['target']='9.0'
        self.assertEqual(self.m.plan(data,self.profiles)['state'],'missing-evidence')
        data=self.ready();data['current']='2.20'
        self.assertEqual(self.m.plan(data,self.profiles)['state'],'missing-evidence')
    def test_missing_target_and_refresh_remain_explicit(self):
        data=self.ready();data['target']=None
        self.assertEqual(self.m.plan(data,self.profiles)['state'],'missing-evidence')
        data=self.ready();data['prerequisites']['sources_refreshed']=False
        r=self.m.plan(data,self.profiles)
        self.assertIn('sources_refreshed',r['missing'])
    def test_workload_scope_is_a_gate(self):
        env=self.environment();env['workload_type']='native CLI'
        self.assertEqual(self.m.select(env,self.profiles,'fraction-limit')['state'],'incompatible')
        env=self.environment();env.pop('workload_type',None)
        self.assertEqual(self.m.select(env,self.profiles,'fraction-limit')['state'],'missing-evidence')
    def test_explicit_local_backport_only(self):
        env=self.environment('3.0.0-vendor');env['scope']='synthetic-lab'
        rules=copy.deepcopy(self.profiles)
        p=copy.deepcopy(rules['profiles'][1]);p.update(id='local-backport',versions=[],exact_raw='3.0.0-vendor',provenance_type='local',scope='synthetic-lab',provenance='synthetic observed API semantics',captured_at='2026-10-18T00:00:00Z');rules['profiles'].append(p)
        self.assertEqual(self.m.select(env,rules,'fraction-limit')['state'],'local-procedure')
        env['scope']='another-cluster'
        self.assertEqual(self.m.select(env,rules,'fraction-limit')['state'],'missing-evidence')
    def test_unrelated_local_conflict_does_not_block(self):
        env=self.environment();env['local_profile']={'component':'runai-cli','workflow':'cli-auth','raw_version':'9.0','provenance':'synthetic','scope':'lab','captured_at':'2026-10-18T00:00:00Z'}
        self.assertEqual(self.m.select(env,self.profiles,'fraction-limit')['state'],'documented-procedure')
    def test_local_profile_scope_does_not_cross_clusters(self):
        env=self.environment();env['scope']='cluster-a';env['local_profile']={'component':'runai-cluster','workflow':'fraction-limit','scope':'cluster-b','raw_version':'9.0','provenance':'synthetic','captured_at':'2026-10-18T00:00:00Z'}
        self.assertEqual(self.m.select(env,self.profiles,'fraction-limit')['state'],'documented-procedure')
    def test_upgrade_requires_independent_component_evidence(self):
        data=self.ready();data.pop('components',None)
        self.assertEqual(self.m.plan(data,self.profiles)['state'],'missing-evidence')
    def test_upgrade_preserves_already_upgraded_control_plane(self):
        data=self.ready();data['components']['runai-control-plane']['raw_version']='3.0'
        result=self.m.plan(data,self.profiles)
        self.assertEqual(result['state'],'documented-plan')
        self.assertNotIn('control-plane',result['stages'])
        self.assertIn('control-plane-verification',result['stages'])
    def test_upgrade_current_conflicts_with_observed_cluster(self):
        data=self.ready();data['components']['runai-cluster']['raw_version']='2.25'
        self.assertEqual(self.m.plan(data,self.profiles)['state'],'conflict')
