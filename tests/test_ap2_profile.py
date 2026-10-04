import sys
import unittest
from pathlib import Path
from rdflib import Graph, Literal, Namespace
from rdflib.namespace import RDF, OWL, XSD
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'tools'))
from check_ap2_profile import load, validate, AP, SOSA
EX=Namespace('https://example.org/ap2/')


class ProfileTests(unittest.TestCase):
    def setUp(self):self.schema,self.data=load(ROOT)
    def test_positive_example(self):self.assertEqual(validate(self.schema,self.data),[])
    def test_source_port_is_not_automatically_operational(self):
        from rdflib.namespace import RDFS
        source=Namespace('https://portwatch.imf.org/ontology/').Port
        self.assertIn((source,RDFS.subClassOf,AP.SourcePortFeature),self.schema)
        self.assertNotIn((source,RDFS.subClassOf,AP.OperationalPort),self.schema)
    def test_trade_location_cannot_be_collapsed_into_port(self):
        self.data.add((EX['port/santos'],RDF.type,AP.TradeLocation))
        self.assertTrue(any('roles collapsed' in x for x in validate(self.schema,self.data)))
    def test_sameas_is_forbidden(self):
        self.data.add((EX['port/santos'],OWL.sameAs,EX['port/hamburg']))
        self.assertTrue(validate(self.schema,self.data))
    def test_pending_candidate_cannot_materialize(self):
        assertion=EX['assertion/pending']
        self.data.add((self.data.value(assertion,AP.subject),self.data.value(assertion,AP.relation),self.data.value(assertion,AP.object)))
        self.assertTrue(any('pending/rejected' in x for x in validate(self.schema,self.data)))
    def test_reversed_relation_fails(self):
        assertion=EX['assertion/0'];subject=self.data.value(assertion,AP.subject);obj=self.data.value(assertion,AP.object)
        self.data.set((assertion,AP.subject,obj));self.data.set((assertion,AP.object,subject))
        self.assertTrue(any('domain/range' in x for x in validate(self.schema,self.data)))
    def test_country_conflict_fails(self):
        self.data.set((EX['port/santos'],AP.countryISO3,Literal('DEU')))
        self.assertTrue(any('Conflicting' in x for x in validate(self.schema,self.data)))
    def test_source_country_conflict_fails(self):
        source=Namespace('https://example.org/ap2/source/portwatch/')['portwatch/port/demoSantos']
        self.data.set((source,AP.countryISO3,Literal('DEU')))
        self.assertTrue(any('country conflict' in x for x in validate(self.schema,self.data)))
    def test_wrong_unit_fails(self):
        self.data.set((EX['measurement/santos/import'],AP.unit,AP.PortCallCount))
        self.assertTrue(any('unit incompatible' in x for x in validate(self.schema,self.data)))
    def test_fractional_calls_fail(self):
        self.data.set((EX['measurement/santos/calls'],AP.value,Literal('1.5',datatype=XSD.decimal)))
        self.assertTrue(any('Invalid measurement' in x for x in validate(self.schema,self.data)))
    def test_nonfinite_mass_fails(self):
        self.data.set((EX['measurement/santos/import'],AP.value,Literal('NaN',datatype=XSD.decimal)))
        self.assertTrue(any('Invalid measurement' in x for x in validate(self.schema,self.data)))
    def test_changed_measurement_cannot_claim_original_source(self):
        self.data.set((EX['measurement/santos/import'],AP.value,Literal('99',datatype=XSD.decimal)))
        self.assertTrue(any('differs from source value' in x for x in validate(self.schema,self.data)))
    def test_activity_cannot_observe_other_port(self):
        self.data.set((EX['activity/santos/2026-01-01'],SOSA.hasFeatureOfInterest,EX['port/hamburg']))
        self.assertTrue(any('activity/result link' in x for x in validate(self.schema,self.data)))
    def test_missing_observation_day_fails(self):
        self.data.remove((EX['observation/santos/2026-01-01'],AP.observedDay,None))
        self.assertTrue(any('observation day' in x for x in validate(self.schema,self.data)))
    def test_source_feature_is_not_canonical_observation_target(self):
        self.data.set((EX['observation/santos/2026-01-01'],AP.observedFeature,EX['record/portwatch/demoSantos']))
        self.assertTrue(any('canonical port feature' in x for x in validate(self.schema,self.data)))
    def test_pdl_node_is_not_physical_facility(self):
        self.data.set((EX['scenario/entity/santos'],AP.representsFacility,EX['scenario/entity/hamburg']))
        self.assertTrue(any('scenario representation' in x for x in validate(self.schema,self.data)))
    def test_result_cannot_be_retyped_as_sosa_activity(self):
        self.data.add((EX['observation/santos/2026-01-01'],RDF.type,SOSA.Observation))
        self.assertTrue(any('separate from SOSA' in x for x in validate(self.schema,self.data)))
    def test_event_episode_is_separate(self):
        self.data.set((EX['episode/invented-disruption/1'],AP.episodeOf,EX['port/santos']))
        self.assertTrue(any('Episode must' in x for x in validate(self.schema,self.data)))
    def test_missing_match_review_fails(self):
        self.data.remove((EX['assertion/0'],AP.reviewer,None))
        self.assertTrue(any('reviewer' in x for x in validate(self.schema,self.data)))
    def test_naive_review_date_fails(self):
        self.data.set((EX['assertion/0'],AP.reviewedAt,Literal('2026-01-03T00:00:00',datatype=XSD.dateTime)))
        self.assertTrue(any('timezone-aware' in x for x in validate(self.schema,self.data)))


if __name__ == '__main__':unittest.main()
