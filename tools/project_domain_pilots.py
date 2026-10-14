"""Bounded real CPPI scores and GEM capacity projection onto the shared result pattern."""
import argparse,json,hashlib
from decimal import Decimal
from pathlib import Path
from rdflib import Graph,URIRef,Literal,Namespace
from rdflib.namespace import RDF,RDFS,XSD
from review_current import ROOT,P,sha,validate_data
DCT=Namespace('http://purl.org/dc/terms/');OLD=Namespace('https://projekt-provider.de/ontology/');M=Namespace(str(P)+'mining#')
BASE='https://projekt-provider.de/resource/current-pilot/'

def record(g,path,url,license,credit):
    source=URIRef(BASE+'source/'+sha(path))
    for pred,value in [(RDF.type,P.SourceRecord),(P.sourceHash,Literal(sha(path))),(P.sourceCheckedOn,Literal('2026-10-14',datatype=XSD.date)),(DCT.source,URIRef(url)),(DCT.rights,Literal(credit)),(RDFS.comment,Literal('Local source-file verification date; original acquisition time unknown.'))]:g.add((source,pred,value))
    if license:g.add((source,DCT.license,URIRef(license)))
    return source

def result(g,node,feature,source,value,kind,unit):
    for pred,obj in [(RDF.type,P.Observation),(P.observedFor,feature),(P.sourceRecord,source),(P.dataKind,Literal('real'))]:g.add((node,pred,obj))
    measurement=URIRef(str(node)+'/measurement');g.add((node,P.hasMeasurement,measurement))
    for pred,obj in [(RDF.type,P.StatisticalMeasurement),(P.measurementValue,Literal(Decimal(str(value)),datatype=XSD.decimal)),(P.measurementKind,kind),(P.hasUnit,P['unit/'+unit])]:g.add((measurement,pred,obj))

def project_cppi(path):
    from provider_cppi.conversion import prepare_payload
    payload=prepare_payload(path);g=Graph();source=record(g,path,'https://openknowledge.worldbank.org/bitstreams/9cf20807-7dcd-4de7-9de2-fdb2d0589a73/download','https://creativecommons.org/licenses/by-nc/3.0/igo/','World Bank and S&P Global Market Intelligence, CPPI2025 annex. PROVIDER: score-only projection, no canonical port identity established.')
    scores=0;negatives=0
    for row in payload['observations']:
        if 'cppi_score' not in row['values']:continue
        feature=URIRef(BASE+'cppi/source-port/'+row['port_key']);node=URIRef(BASE+'cppi/result/'+hashlib.sha256(json.dumps([sha(path),row['port_key'],row['year']]).encode()).hexdigest())
        result(g,node,feature,source,row['values']['cppi_score'],P.CPPIIndexScore,'DimensionlessIndex')
        for pred,obj in [(RDF.type,URIRef(str(P)+'source/cppi#ContainerPortPerformanceObservation')),(P.referenceYear,Literal(str(row['year']),datatype=XSD.gYear)),(P.sourceValue,Literal(row['values']['cppi_score'])),(DCT.identifier,Literal(f"Annex row {row['source_row']}"))]:g.add((node,pred,obj))
        row_content=json.dumps({'workbook_sha256':sha(path),'year':row['year'],'source_row':row['source_row'],'cells':row['cells']},sort_keys=True,ensure_ascii=False,separators=(',',':'))
        g.add((node,P.sourceHash,Literal(hashlib.sha256(row_content.encode()).hexdigest())))
        g.add((node,P.sourceCheckedOn,Literal('2026-10-14',datatype=XSD.date)))
        # Source feature remains explicitly distinct from accepted operational-port identity.
        g.add((feature,RDFS.label,Literal(row['port_name'])));scores+=1;negatives+=Decimal(row['values']['cppi_score'])<0
    return g,{'source_sha256':sha(path),'source_observations':len(payload['observations']),'projected_scores':scores,'negative_scores':negatives,'scope':'Full actual combined score series only; ranks/components/operational metrics remain in source payload and are outside this projection. No automatic canonical port linking.'}

def project_gem(path,output,sheet,limit):
    from provider_mining_rdf.converters.gem import convert_gem
    raw=output/'gem-source.ttl';convert_gem(path,raw,sheet=sheet,tracker='coal',limit=limit)
    source_graph=Graph().parse(raw);g=Graph();source=record(g,path,'https://globalenergymonitor.org/projects/global-coal-mine-tracker/',None,'Global Energy Monitor, Global Coal Mine Tracker, May2026. PROVIDER: bounded capacity projection; no company/facility identity reconciliation.')
    count=0;skipped=0
    for node in source_graph.subjects(RDF.type,OLD.CapacityObservation):
        values=list(source_graph.objects(node,OLD.numericValue));unit=list(source_graph.objects(node,OLD.unitCode));facility=list(source_graph.objects(node,OLD.observedFacility))
        if not values:skipped+=1;continue
        if len(values)!=1 or unit!=[Literal('tpa')] or len(facility)!=1:raise ValueError('Ambiguous or unsupported GEM capacity record')
        projected=URIRef(str(node)+'/current-result');result(g,projected,facility[0],source,values[0],P.ProductionCapacity,'TonnePerYear');g.add((projected,RDF.type,M.CapacityObservation));g.add((facility[0],RDF.type,P.Facility));count+=1
    return g,{'source_sha256':sha(path),'raw_rdf_sha256':sha(raw),'selected_sheet':sheet,'row_limit':limit,'rights_status':'local workbook reuse not cleared; no license asserted','capacity_results':count,'capacity_without_value':skipped,'scope':'First selected source rows only. Converter scales Mtpa to tonnes/year. Capacity is not realized production; no missing-value imputation, ICMM/GEM identity links or operator approval.'}

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--cppi',type=Path,required=True);p.add_argument('--gem',type=Path,required=True);p.add_argument('--gem-sheet',default='Non-closed mines');p.add_argument('--gem-limit',type=int,default=20);p.add_argument('--output',type=Path,required=True);a=p.parse_args();a.output.mkdir(parents=True,exist_ok=True)
    model_pin=sha(ROOT/'docs/current-release.json')
    c,cp=project_cppi(a.cppi);m,mp=project_gem(a.gem,a.output,a.gem_sheet,a.gem_limit);report={}
    for name,g,proof in [('cppi',c,cp),('mining',m,mp)]:
        if not len(g):raise ValueError('Empty domain pilot')
        path=a.output/(name+'-provider.nt');path.write_text(''.join(sorted(g.serialize(format='nt').splitlines(keepends=True))))
        conforms,validation=validate_data(g,meta=False);validation.serialize(a.output/(name+'-shacl.ttl'),format='turtle');report[name]={**proof,'passed':conforms,'triples':len(g),'rdf_sha256':sha(path)}
    union=c+m;rows=list(union.query('PREFIX p: <https://projekt-provider.de/ontology/> SELECT ?kind (COUNT(?measurement) AS ?count) WHERE {?result p:hasMeasurement ?measurement . ?measurement p:measurementKind ?kind} GROUP BY ?kind'))
    report.update({'passed':all(report[x]['passed'] for x in ['cppi','mining']),'common_query_counts':{str(k):int(n) for k,n in rows},'adapter_sha256':sha(Path(__file__)),'model_manifest_sha256':sha(ROOT/'docs/current-release.json')})
    if sha(ROOT/'docs/current-release.json')!=model_pin:raise ValueError('Model changed during validation; rerun')
    (a.output/'domain-pilots.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report));return 0 if report['passed'] else 1
if __name__=='__main__':raise SystemExit(main())
