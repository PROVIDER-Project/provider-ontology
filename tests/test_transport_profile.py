"""Transport profile rejects inconsistent endpoints and route modalities."""
import unittest,sys
from pathlib import Path
from rdflib import Graph,Namespace,Literal
from rdflib.namespace import RDF,RDFS,OWL
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'tools'))
from review_current import load,validate_data,P
N=Namespace(str(P)+'network#')
class TransportProfileTests(unittest.TestCase):
 def fixture(self):return Graph().parse(ROOT/'examples/current/transport-example.ttl')
 def test_wrong_traversal_endpoint_rejected(self):
  g=self.fixture();edge=next(g.subjects(RDF.type,N.Traversal));ends=set(g.objects(edge,N.fromJunction))|set(g.objects(edge,N.toJunction));wrong=next(n for n in g.subjects(RDF.type,N.Junction) if n not in ends);g.set((edge,N.toJunction,wrong));self.assertFalse(validate_data(g,profile='transport',meta=False)[0])
 def test_mixed_mode_route_rejected(self):
  g=self.fixture();path=next(s for s in g.subjects(RDF.type,N.TransportPath) if (s,N.transportMode,Literal('road')) in g);g.set((path,N.transportMode,Literal('rail')));self.assertFalse(validate_data(g,profile='transport',meta=False)[0])
 def test_route_is_information_and_roles_are_route_specific(self):
  _,schema=load(profile='transport');self.assertIn((N.Route,RDFS.subClassOf,P.Route),schema);self.assertNotIn((N.Route,RDFS.subClassOf,N.Network),schema);self.assertIn((N.routeRole,OWL.deprecated,Literal(True)),schema);g=self.fixture();self.assertFalse(list(g.triples((None,N.routeRole,None))));self.assertTrue(list(g.triples((None,N.stepRole,None))))
if __name__=='__main__':unittest.main()
