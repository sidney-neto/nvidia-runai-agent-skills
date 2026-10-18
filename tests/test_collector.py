import subprocess
import unittest
from unittest.mock import patch
from test_helpers import module

class Collector(unittest.TestCase):
    def test_explicit_projected_reads(self):
        m=module('runai-context-discovery','collect')
        commands=m.commands('cluster-a','team-a',['pod-a'],['node-a'])
        for field,command in commands:
            self.assertEqual(command[0],'kubectl')
            self.assertIn('--context=cluster-a',command)
            self.assertIn('get',command)
            self.assertTrue(any(arg.startswith('--output=jsonpath=') for arg in command))
            self.assertFalse(set(command)&{'apply','delete','patch','upgrade','drain','exec','logs','secrets','config'})
        self.assertTrue(all('env' not in str(command) for _,command in commands))
    def test_invalid_target_cannot_inject_flags(self):
        m=module('runai-context-discovery','collect')
        for target in ('--all-namespaces','pod/name','a b','a;id'):
            with self.assertRaises(ValueError):m.commands('ctx','ns',[target],[])
    def test_failure_is_distinct_and_does_not_echo(self):
        m=module('runai-context-discovery','collect')
        with patch.object(m,'run',return_value=(1,'','Forbidden SYNTHETIC_SECRET')):
            result=m.collect('ctx','ns',['pod'],[])
        self.assertEqual(result['evidence'][0]['state'],'permission-denied')
        self.assertNotIn('SYNTHETIC_SECRET',str(result))
        with patch.object(m,'run',side_effect=FileNotFoundError):
            self.assertEqual(m.collect('ctx','ns',['pod'],[])['evidence'][0]['state'],'unavailable')
        with patch.object(m,'run',side_effect=subprocess.TimeoutExpired(['kubectl'],15)):
            self.assertEqual(m.collect('ctx','ns',['pod'],[])['evidence'][0]['state'],'timeout')
    def test_mcp_absent_authorized_kubernetes_alternative(self):
        m=module('runai-context-discovery','collect')
        with patch.object(m,'run',return_value=(0,'Pending','')):
            result=m.collect('ctx','ns',['pod'],[])
        self.assertEqual(result['evidence'][0]['value'],'Pending')
        self.assertIn('kubectl',result['adapter'])
    def test_output_bound_on_synthetic_process(self):
        import sys
        m=module('runai-context-discovery','collect')
        with self.assertRaises(ValueError):m.run([sys.executable,'-c','print("x" * 9000)'])
        self.assertEqual(m.run([sys.executable,'-c','print("Pending")'])[1].strip(),'Pending')
