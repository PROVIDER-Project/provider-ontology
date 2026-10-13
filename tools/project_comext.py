"""Explicit Comext source-to-PROVIDER projection; original source graph is untouched."""
from pathlib import Path
from datetime import datetime
import argparse
import hashlib
import json
from rdflib import Graph,Namespace,URIRef,Literal
from rdflib.namespace import RDF,DCTERMS,XSD
from review_current import P,validate_data
CX=Namespace('https://projekt-provider.de/vocab/comext/')
PROV=Namespace('http://www.w3.org/ns/prov#')


def project(source,artifact_id,*,data_kind):
    if data_kind not in {'real','synthetic'}:raise ValueError('Explicit real/synthetic scope required')
    graph=Graph();base=Namespace('https://projekt-provider.de/id/ontology-review/comext/'+artifact_id+'/')
    cells=set(source.subjects(RDF.type,CX.Cell))
    if not cells:raise ValueError('No Comext cells found')
    def iri(node):return base[hashlib.sha256(str(node).encode()).hexdigest()]
    source_records=set(source.subjects(CX.sha256,None))
    for node in source_records:
        target=iri(node);graph.add((target,RDF.type,P.SourceRecord));graph.add((target,P.sourceHash,source.value(node,CX.sha256)));graph.add((target,P.acquiredAt,source.value(node,CX.acquiredAt)));graph.add((target,PROV.wasDerivedFrom,node))
        for value in source.objects(node,CX.providerUpdated):
            graph.add((target,P.providerUpdatedAt,Literal(datetime.fromisoformat(str(value)).isoformat(),datatype=XSD.dateTime)))
        for value in source.objects(node,DCTERMS.source):graph.add((target,DCTERMS.source,value))
    for node in source.subjects(RDF.type,CX.AnnualSelection):
        target=iri(node)
        for cls in [P.CNSelection,P.ClassificationSelection]:graph.add((target,RDF.type,cls))
        for old,new in [(CX.productCode,P.productCode),(CX.classificationYear,P.classificationYear),(CX.annualCNScheme,P.classificationScheme),(CX.cn8MemberCode,P.memberCode),(CX.comparisonPolicy,P.comparisonPolicy),(CX.hsEdition,P.hsEdition),(CX.hs2022BoundaryQualification,P.boundaryQualification)]:
            for value in source.objects(node,old):graph.add((target,new,value))
        graph.add((target,PROV.wasDerivedFrom,node))
    def dimensions(node,target):
        for old,new in [(CX.reporter,P.reporter),(CX.partner,P.partner),(CX.partnerBasis,P.partnerBasis),(CX.flow,P.flowCode),(CX.productCode,P.productCode),(CX.providerStatus,P.providerStatus)]:
            for value in source.objects(node,old):graph.add((target,new,value))
        for selection in source.objects(node,CX.selection):graph.add((target,P.classificationConcept,iri(selection)))
        for record in source.objects(node,PROV.wasDerivedFrom):
            if record not in source_records:raise ValueError('Statistical cell lacks a capture record')
            graph.add((target,P.sourceRecord,iri(record)))
        graph.add((target,P.dataKind,Literal(data_kind)));graph.add((target,PROV.wasDerivedFrom,node))
    def measure(node,predicate,value):
        metric={'VALUE_IN_EUROS':P.TradeValue,'QUANTITY_IN_100KG':P.TradeMass}[str(source.value(node,CX.indicator))]
        target=URIRef(str(iri(node))+'/'+str(predicate).rsplit('/',1)[-1])
        graph.add((target,RDF.type,P.StatisticalMeasurement));graph.add((target,P.measurementKind,metric));graph.add((target,P.hasUnit,P['unit/Euro'] if metric==P.TradeValue else P['unit/Kilogram']));graph.add((target,P.measurementValue,value));return target
    for node in cells:
        target=iri(node);presence=source.value(node,CX.presence);dimensions(node,target)
        for cls in [P.StatisticalCell,P.TradeCell]:graph.add((target,RDF.type,cls))
        graph.add((target,P.presence,presence));graph.add((target,P.referenceMonth,source.value(node,CX.referenceMonth)))
        if str(presence)=='missing':graph.add((target,RDF.type,P.MissingCell))
        else:
            graph.add((target,RDF.type,P.StatisticalObservation));graph.add((target,P.hasMeasurement,measure(node,P.hasMeasurement,source.value(node,CX.value))))
    for node in source.subjects(RDF.type,CX.AnnualCoverage):
        target=iri(node);dimensions(node,target);graph.add((target,RDF.type,P.AnnualCoverage));graph.add((target,P.referenceYear,Literal(str(source.value(node,CX.year)),datatype=XSD.gYear)))
        for old,new in [(CX.observedMonths,P.observedMonths),(CX.complete,P.complete)]:graph.add((target,new,source.value(node,old)))
        for old,new in [(CX.observedSum,P.observedSum),(CX.annualTotal,P.annualTotal)]:
            for value in source.objects(node,old):graph.add((target,new,measure(node,new,value)))
    for node in source.subjects(RDF.type,URIRef('http://purl.org/linked-data/cube#DataSet')):
        target=iri(node);graph.add((target,RDF.type,P.SourceDataset));graph.add((target,PROV.wasDerivedFrom,node));graph.add((target,P.dataKind,Literal(data_kind)))
        for pred in [DCTERMS.title,DCTERMS.bibliographicCitation,DCTERMS.rights]:
            for value in source.objects(node,pred):graph.add((target,pred,value))
        for pred in [CX.modificationNotice,CX.nonresponsibilityNotice]:
            for value in source.objects(node,pred):graph.add((target,P.changeNotice,value))
    if len(set(graph.subjects(RDF.type,P.StatisticalCell)))!=len(cells):raise ValueError('Projection coverage mismatch')
    return graph


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--bundle',type=Path,required=True);parser.add_argument('--output',type=Path,required=True);parser.add_argument('--validate',action='store_true');args=parser.parse_args()
    if args.output.exists() or args.output.with_suffix('.json').exists():raise ValueError('Preserve previous projection outputs; choose a new name')
    # Requires the packaged converter or sibling provider-datasets/src on PYTHONPATH.
    from provider_comext.converter import inspect
    manifest=inspect(args.bundle);source=Graph().parse(args.bundle/'dataset.nt',format='nt')
    config=json.loads((args.bundle/'build-config.json').read_text());graph=project(source,manifest['artifact_id'],data_kind=config['data_kind'])
    report={'source_artifact_id':manifest['artifact_id'],'source_rdf_sha256':manifest['files']['dataset.nt'],'model_version':'0.3.0-rc1','model_manifest_sha256':hashlib.sha256((Path(__file__).resolve().parents[1]/'docs/current-release.json').read_bytes()).hexdigest(),'adapter_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'namespace':str(P),'source_untouched':True,'cells':len(set(graph.subjects(RDF.type,P.StatisticalCell))),'missing':len(set(graph.subjects(RDF.type,P.MissingCell))),'triples':len(graph),'full_shacl':None,'limits':'Comext-only explicit adapter; no other production-source migration, no public release or partner acceptance.'}
    if args.validate:
        passed,validation=validate_data(graph);report['full_shacl']=passed
        if not passed:
            validation.serialize('/tmp/provider-comext-projection-failure.ttl',format='turtle');raise ValueError('Canonical projection failed SHACL')
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(''.join(sorted(f'{s.n3()} {p.n3()} {o.n3()} .\n' for s,p,o in graph)))
    report['rdf_sha256']=hashlib.sha256(args.output.read_bytes()).hexdigest();args.output.with_suffix('.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))

if __name__=='__main__':main()
