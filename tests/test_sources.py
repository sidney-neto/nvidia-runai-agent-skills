import copy
from datetime import date
import importlib.util
from pathlib import Path
import unittest
ROOT=Path(__file__).resolve().parents[1]
def load():
    spec=importlib.util.spec_from_file_location('sources',ROOT/'scripts/check_sources.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
class Sources(unittest.TestCase):
    def test_changed_redirected_unavailable_preserve_review(self):
        m=load();record={'id':'synthetic','url':'https://example.com/a','resolved_url':'https://example.com/a','sha256':'previous','reviewed_at':'2026-01-01'};before=copy.deepcopy(record)
        result=m.assess(record,{'resolved_url':'https://example.com/b','sha256':'new','status':'available'},date(2026,10,18),90)
        self.assertEqual(set(result['states']),{'changed','redirected','aging'})
        self.assertEqual(record,before)
        result=m.assess(record,{'status':'unavailable'},date(2026,10,18),90)
        self.assertIn('unavailable',result['states'])
        self.assertEqual(record,before)
    def test_unsafe_source_rejected(self):
        m=load()
        for url in ('http://example.com','https://user:password@docs.nvidia.com/a','https://127.0.0.1/a','file:///etc/passwd'):
            with self.assertRaises(ValueError):m.validate_url(url)
