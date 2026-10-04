import importlib.util
import json
import unittest
from pathlib import Path
from rdflib import Graph, URIRef, Literal, Namespace
from rdflib.namespace import RDF
from rdflib.util import from_n3
ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('shacl_runner', ROOT/'tools/validate_ap2_shacl.py')
runner = importlib.util.module_from_spec(spec); spec.loader.exec_module(runner)
AP = runner.AP
class ShaclTests(unittest.TestCase):
 def test_valid_fixture_and_no_mutation(self):
  g=runner.example_graph(ROOT); before=set(g)
  summary, report=runner.validate_graph(ROOT,g,data_kind='synthetic')
  self.assertTrue(summary['conforms']); self.assertEqual(set(g),before)
 def test_negative_cases(self):
  for case in json.loads((ROOT/'examples/ap2-shacl/negative-cases.json').read_text()):
   with self.subTest(case=case['name']):
    g=runner.example_graph(ROOT); s=URIRef(case['subject']); p=URIRef(case['predicate'])
    if case['remove_existing']: g.remove((s,p,None))
    if case['replacement']: g.add((s,p,from_n3(case['replacement'])))
    summary,_=runner.validate_graph(ROOT,g,data_kind='synthetic')
    self.assertFalse(summary['conforms'],case['name']); self.assertTrue(summary['validation_results'])
 def test_empty_and_unrelated_are_rejected(self):
  for g in [Graph(), Graph().add((URIRef('https://example.org/a'), RDF.type, URIRef('https://example.org/B')))]:
   self.assertFalse(runner.validate_graph(ROOT,g)[0]['conforms'])
 def test_source_profile_cannot_hide_canonical_errors(self):
  self.assertFalse(runner.validate_graph(ROOT,runner.example_graph(ROOT),profile='source')[0]['conforms'])
 def test_point_bounds(self):
  g=runner.example_graph(ROOT); geo=Namespace('http://www.opengis.net/ont/geosparql#')
  point=next(g.subjects(geo.asWKT,None)); g.set((point,geo.asWKT,Literal('POINT (181 0)',datatype=geo.wktLiteral)))
  self.assertFalse(runner.validate_graph(ROOT,g)[0]['conforms'])
if __name__=='__main__': unittest.main()
