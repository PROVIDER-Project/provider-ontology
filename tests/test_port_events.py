"""Source uncertainty and scope may not silently become realized whole-port impact."""
import sys,unittest
from pathlib import Path
from rdflib import Graph,Namespace,Literal
from rdflib.namespace import RDF,DCTERMS,PROV,XSD
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'tools'))
from validate_port_events import check,load,PROFILE
P=Namespace('https://projekt-provider.de/ontology/');PE=Namespace(str(P)+'profiles/port-events#');B=Namespace('https://example.org/provider/port-event-fixture/')
class CoarsePortEventTests(unittest.TestCase):
 def fixture(self):return Graph().parse(ROOT/PROFILE/'examples.ttl')
 def test_all_evidence_categories_validate_without_mutation(self):
  g=self.fixture();before=set(g);self.assertTrue(check(g)[0]);self.assertEqual(before,set(g))
 def test_semantic_promotions_and_fabricated_precision_rejected(self):
  cases=[
   ('exposure to restriction',B['exposure-claim'],DCTERMS.type,PE.OperationalRestriction),
   ('exposure becomes reported',B['exposure-claim'],P.assertionMode,P.Reported),
   ('whole port instead of passage',B['planned-passage-claim'],RDF.object,B.port),
   ('partial becomes complete',B['partial-port-claim'],DCTERMS.extent,PE.FullTarget),
   ('announcement becomes observed report',B['planned-passage-claim'],P.assertionMode,P.Reported),
   ('rail restriction invented',B['planned-passage-claim'],DCTERMS.subject,PE.RailAccess),
   ('time text becomes publication timestamp',B.exposure,P.startTime,Literal('2026-01-03T00:00:00Z',datatype=XSD.dateTime)),
   ('conflicting end picked',B.conflicting,P.endTime,Literal('2026-01-03T00:00:00Z',datatype=XSD.dateTime)),
   ('negative time interval',B['planned-passage'],P.endTime,Literal('2026-01-01T00:00:00Z',datatype=XSD.dateTime)),
   ('naive capture time',B.source,P.acquiredAt,Literal('2026-01-03T10:00:00',datatype=XSD.dateTime))]
  for name,s,p,o in cases:
   with self.subTest(name=name):
    g=self.fixture();g.set((s,p,o));self.assertFalse(check(g)[0],name)
 def test_unguarded_affects_and_causes_rejected(self):
  for pred in [P.affects,P.causes]:
   g=self.fixture();g.add((B.exposure,pred,B.port));self.assertFalse(check(g)[0])
 def test_derived_effect_requires_assumption(self):
  g=self.fixture();g.remove((B['possible-impact-claim'],P.assumptionNote,None));self.assertFalse(check(g)[0])
 def test_source_hash_is_required(self):
  g=self.fixture();g.remove((B.source,P.sourceHash,None));self.assertFalse(check(g)[0])
 def test_profile_reuses_base_without_new_event_classes(self):
  from rdflib.namespace import OWL
  descriptor,g,_=load();self.assertEqual(descriptor['base_version'],'0.3.0-rc3')
  profile=Graph().parse(ROOT/PROFILE/'profile.ttl');self.assertFalse(list(profile.subjects(RDF.type,OWL.Class)))
if __name__=='__main__':unittest.main()
