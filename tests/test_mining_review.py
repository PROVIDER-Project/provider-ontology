from pathlib import Path
import unittest
from rdflib import Graph,URIRef,Literal
from rdflib.namespace import RDF
from pyshacl import validate

ROOT=Path(__file__).parents[1]/'ontology/mining'
M='https://projekt-provider.de/ontology/'
class MiningReview(unittest.TestCase):
    def fixture(self,relation='ExactAssetMatch'):
        g=Graph();a=URIRef('https://example.org/assertion')
        for p,o in [('sourceEntity',URIRef('https://example.org/mine')),('targetEntity',URIRef('https://example.org/target')),('alignmentRelation',URIRef(M+relation)),('reviewStatus',Literal('accepted_by_reviewer')),('reviewNote',Literal('Synthetic explicit review')),('reviewEvidence',Literal('Own synthetic evidence'))]:g.add((a,URIRef(M+p),o))
        g.add((a,RDF.type,URIRef(M+'EntityAlignmentAssertion')));g.add((a,URIRef('http://www.w3.org/ns/prov#wasAttributedTo'),Literal('Synthetic reviewer')))
        return g,a
    def check(self,g):return validate(g,shacl_graph=Graph().parse(ROOT/'provider-mining-reviewed-shacl.ttl'),do_owl_imports=False)[0]
    def test_syntax_and_reviewed_acceptance(self):
        for p in ROOT.glob('*.ttl'):self.assertGreater(len(Graph().parse(p)),0)
        g,a=self.fixture();self.assertTrue(self.check(g))
    def test_candidate_is_not_releaseable(self):
        g,a=self.fixture();p=URIRef(M+'reviewStatus');g.set((a,p,Literal('auto_accepted')));self.assertFalse(self.check(g))
    def test_structural_relation_cannot_merge(self):
        g,a=self.fixture('AssetPartOfComplex');self.assertTrue(self.check(g));g.add((a,URIRef(M+'mappedConcept'),URIRef('https://example.org/canonical')));self.assertFalse(self.check(g))
    def test_conflict_blocks_release(self):
        g,a=self.fixture();g.add((a,URIRef(M+'hardConflict'),Literal('country mismatch')));self.assertFalse(self.check(g))
