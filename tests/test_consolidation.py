"""Meaningful regression checks for profile boundaries and real-source semantics."""
import json,sys,tempfile,shutil,unittest
from pathlib import Path
from rdflib import Graph,Namespace,Literal,URIRef
from rdflib.namespace import RDF,RDFS,OWL,XSD
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'tools'))
import review_current as review
from project_genesis import project
P=review.P;M=Namespace(str(P)+'mining#');CP=Namespace(str(P)+'source/cppi#')

class ConsolidationTests(unittest.TestCase):
    def test_slim_profiles_have_exact_recursive_boundaries(self):
        _,statistics=review.load(profile='statistics');_,mining=review.load(profile='mining');_,bfo=review.load(profile='bfo')
        self.assertIn((P.StatisticalObservation,RDF.type,OWL.Class),statistics)
        self.assertNotIn((M.MiningObservation,RDF.type,OWL.Class),statistics)
        self.assertNotIn((CP.ContainerPortPerformanceObservation,RDF.type,OWL.Class),statistics)
        self.assertIn((M.MiningObservation,RDF.type,OWL.Class),mining)
        self.assertNotIn((URIRef('http://purl.obolibrary.org/obo/bfo.owl'),RDF.type,OWL.Ontology),mining)
        self.assertIn((URIRef('http://purl.obolibrary.org/obo/bfo.owl'),RDF.type,OWL.Ontology),bfo)
        with self.assertRaisesRegex(ValueError,'Unknown model profile'):review.load(profile='typo')
    def test_tampered_profile_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            for name in ['ontology','shapes','docs']:
                shutil.copytree(ROOT/name,root/name)
            (root/'ontology/current/profiles/statistics.ttl').write_text('# broken')
            with self.assertRaisesRegex(ValueError,'Changed profile'):review.load(root,profile='statistics')
    def test_source_precision_and_cppis_result_activity_boundary(self):
        data=Graph().parse(ROOT/'examples/current/ap2-example.ttl');source=next(data.subjects(RDF.type,P.SourceRecord));data.remove((source,P.acquiredAt,None));data.add((source,P.sourceCheckedOn,Literal('2026-10-14',datatype=XSD.date)))
        self.assertTrue(review.validate_data(data,meta=False)[0]);data.remove((source,P.sourceCheckedOn,None));self.assertFalse(review.validate_data(data,meta=False)[0])
        _,schema=review.load(profile='maritime')
        for cls in [CP.ContainerPortPerformanceObservation,CP.CPPIStratifiedPortTimeObservation]:
            self.assertIn(P.Observation,review.ancestors(schema,cls));self.assertNotIn(review.SOSA.Observation,review.ancestors(schema,cls))
    def test_genesis_preserves_suppression_units_scopes_and_original_tokens(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);folder=root/'catalog/ap21/genesis';folder.mkdir(parents=True)
            common={'checked_on':'2026-10-08','table_url':'https://example.org/table','license':'https://example.org/license','attribution':'Test source'}
            for name in ['capture-manifest.json','production-capture-manifest.json','gp9-publisher-manifest.json']:(folder/name).write_text(json.dumps(common))
            (folder/'price-observations.csv').write_text('series_code,label,period,value,value_unit,value_q\nGP19-1,Price,2022-01,"0,0",2021=100,e\n')
            (folder/'production-observations.csv').write_text('series_code,label,period,value,value_unit,value_q,adjustment\nWZ08-1,Index,2022-01,"90,5",2021=100,p,Originalwerte\n')
            (folder/'gp9-publisher-observations.csv').write_text('series_code,label,period,production_scope,unit,source_value,numeric_value,source_marker,value_q\nGP19-2,Product,2022-Q1,total,t-N,-,,-,\nGP19-2,Product,2022-Q1,sold,t-N,20,20,,e\n')
            g,proof=project(root);self.assertEqual(proof['counts']['cells'],4);self.assertEqual(proof['counts']['missing'],1)
            missing=next(g.subjects(RDF.type,P.MissingCell));self.assertFalse(list(g.objects(missing,P.hasMeasurement)));self.assertEqual(str(next(g.objects(missing,P.sourceValue))),'-')
            nitrogen=next(g.subjects(P.measurementKind,P.NitrogenProductionMass));self.assertIn((nitrogen,P.hasUnit,P['unit/TonneNitrogen']),g)
            self.assertEqual(len(set(g.subjects(P.productionScope,None))),2)
            self.assertTrue(review.validate_data(g,meta=False)[0]);self.assertEqual(set(g),set(project(root)[0]))

if __name__=='__main__':unittest.main()
