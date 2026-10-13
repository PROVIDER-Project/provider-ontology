"""Regression tests for the HTTPS candidate, competency questions and semantic boundaries."""
import json
from pathlib import Path
import sys
import unittest
from rdflib import Graph,Literal,URIRef,Namespace
from rdflib.namespace import RDF,RDFS,OWL,XSD
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'tools'))
import review_current as review
from project_comext import project,CX,PROV
P=review.P;E=Namespace('https://example.org/provider-review/')

class CurrentReviewTests(unittest.TestCase):
    def fixture(self):return Graph().parse(ROOT/'examples/current/ap2-example.ttl')
    def test_structural_review_and_all_competency_questions(self):
        self.assertTrue(review.audit(ROOT)['passed'])
        questions=review.competency_questions(ROOT)
        self.assertEqual(len(questions),31);self.assertTrue(all(q['passed'] for q in questions))
    def test_positive_shacl_without_mutating_data(self):
        data=self.fixture();before=set(data)
        self.assertTrue(review.validate_data(data)[0]);self.assertEqual(set(data),before)
    def test_semantic_negative_cases(self):
        cases=[
          ('missing value',E.missing,P.hasMeasurement,E['zero-value']),
          ('false zero',E['zero-value'],P.measurementValue,Literal('7',datatype=XSD.decimal)),
          ('wrong CN year',E['selection-2022'],P.classificationYear,Literal(2021)),
          ('index in kilograms',E['price-index'],P.hasUnit,P['unit/Kilogram']),
          ('partial annual total',E['partial-year'],P.annualTotal,E['partial-sum']),
          ('result as activity',E.present,RDF.type,review.SOSA.Observation),
          ('naive acquisition',E.source,P.acquiredAt,Literal('2026-10-06T00:00:00',datatype=XSD.dateTime)),
          ('invalid GP quarter',E['genesis-quarter'],P.referenceQuarter,Literal('2022-Q5')),
          ('modeled route as voyage',E['modeled-route'],RDF.type,P.ObservedVoyage),
          ('negative capacity',E.capacity,P.measurementValue,Literal('-1',datatype=XSD.decimal)),
          ('scenario materialized',E.hazard,P.causes,E.plant)]
        for name,s,p,o in cases:
            with self.subTest(name=name):
                data=self.fixture()
                if name not in ['missing value','partial annual total','result as activity','modeled route as voyage','scenario materialized']:data.remove((s,p,None))
                data.add((s,p,o));self.assertFalse(review.validate_data(data,meta=False)[0],name)
    def test_index_requires_base(self):
        data=self.fixture();data.remove((E['price-index'],P.indexBase,None))
        self.assertFalse(review.validate_data(data,meta=False)[0])
    def test_route_step_positions_are_per_route(self):
        data=self.fixture();N=Namespace(str(P)+'network#')
        data.set((E['step-b'],N.inRoute,E.route));data.set((E['step-b'],N.sequenceIndex,Literal(0,datatype=XSD.nonNegativeInteger)))
        self.assertFalse(review.validate_data(data,meta=False)[0])
    def test_schema_keeps_roles_and_quantities_distinct(self):
        _,g=review.load(ROOT);M=Namespace(str(P)+'mining#');H=Namespace(str(P)+'hazard#')
        self.assertNotIn(review.SOSA.Observation,review.ancestors(g,M.MiningObservation))
        self.assertNotIn(P.DisruptionEvent,review.ancestors(g,H.HazardEvent))
        self.assertNotIn((P.Commodity,RDFS.subClassOf,Namespace('http://www.w3.org/2004/02/skos/core#').Concept),g)
        self.assertIn((P.unit,RDF.type,OWL.DatatypeProperty),g)
        self.assertIn((P.hasUnit,RDF.type,OWL.ObjectProperty),g)
    def test_all_dataset_registry_entries_have_explicit_coverage(self):
        d=json.loads((ROOT/'docs/dataset-coverage.json').read_text())
        self.assertEqual(len(d['sources']),34);self.assertEqual(len({s['source_id'] for s in d['sources']}),34)
        for source in d['sources']:
            self.assertTrue(source['model_terms']);self.assertTrue(source['competency_questions'])
            self.assertIn(source['integration_status'],['comext-real-projection-validated','legacy-profile-kept; adapter-pending','model-only; no production-adapter'])
    def test_legacy_pins_and_local_drafts_preserved(self):
        d=json.loads((ROOT/'docs/review/2026-10-13/inventory-before.json').read_text())
        for item in d['files']:
            path=ROOT/item['path']
            drafts={'provider-main.ttl':'provider-main-root-draft.ttl','ontology/provider-event.ttl':'provider-event-draft.ttl'}
            if not path.exists() and item['path'] in drafts:
                path=ROOT/'docs/review/2026-10-13/inputs'/drafts[item['path']]
            self.assertEqual(review.sha(path),item['sha256'],item['path'])
    def test_explicit_comext_projection_preserves_source_and_missingness(self):
        g=Graph();base=Namespace('https://example.org/source/');record=base.capture;selection=base.selection
        for triple in [(record,CX.sha256,Literal('a'*64)),(record,CX.acquiredAt,Literal('2026-10-06T08:00:00Z',datatype=XSD.dateTime)),(selection,RDF.type,CX.AnnualSelection),(selection,CX.classificationYear,Literal(2022)),(selection,CX.productCode,Literal('310210')),(selection,CX.annualCNScheme,URIRef('http://data.europa.eu/xsp/cn2022/cn2022')),(selection,CX.cn8MemberCode,Literal('31021010')),(selection,CX.comparisonPolicy,Literal('qualified annual selection'))]:g.add(triple)
        for name,presence,value in [('zero','explicit-zero','0'),('missing','missing',None)]:
            node=base[name]
            for pred,obj in [(RDF.type,CX.Cell),(CX.presence,Literal(presence)),(CX.referenceMonth,Literal('2022-01',datatype=XSD.gYearMonth)),(CX.selection,selection),(PROV.wasDerivedFrom,record),(CX.indicator,Literal('QUANTITY_IN_100KG'))]:g.add((node,pred,obj))
            if value is not None:g.add((node,CX.value,Literal(value,datatype=XSD.decimal)))
        before=set(g);projected=project(g,'synthetic-test',data_kind='synthetic')
        self.assertEqual(set(g),before);self.assertEqual(len(set(projected.subjects(RDF.type,P.MissingCell))),1)
        self.assertTrue(review.validate_data(projected,meta=False)[0])
        self.assertEqual(set(projected),set(project(g,'synthetic-test',data_kind='synthetic')))

if __name__=='__main__':unittest.main()
