"""Pinned OWL2 DL profile/coherence and semantic probes; no runtime network imports."""
import argparse,hashlib,json,subprocess
from pathlib import Path
from rdflib import Graph,URIRef,BNode
from rdflib.namespace import RDF,RDFS,OWL
from review_current import load,sha,ROOT,P

def flatten(graph):
    result=Graph();result+=graph
    # Flatten only module headers/imports. Preserve every logical axiom and individual.
    for header in list(result.subjects(RDF.type,OWL.Ontology)):
        result.remove((header,None,None))
    result.remove((None,OWL.imports,None))
    result.add((URIRef('urn:provider:closed-model'),RDF.type,OWL.Ontology))
    return result

def run(jar,args,path):
    result=subprocess.run(['java','-jar',str(jar),*args],capture_output=True,text=True,timeout=180)
    path.write_text(result.stdout+result.stderr)
    return result.returncode

def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--robot-jar',type=Path,required=True);parser.add_argument('--output',type=Path,required=True);a=parser.parse_args()
    lock=json.loads((ROOT/'docs/reasoner-lock.json').read_text())
    if sha(a.robot_jar)!=lock['robot']['sha256']:raise ValueError('Unpinned ROBOT binary')
    if sha(ROOT/lock['bfo']['path'])!=lock['bfo']['sha256']:raise ValueError('Changed BFO import')
    a.output.mkdir(parents=True,exist_ok=True);manifest,schema=load();graph=flatten(schema)
    model=a.output/'closed-model.ttl';graph.serialize(model,format='turtle')
    dl=run(a.robot_jar,['validate-profile','--profile','DL','--input',str(model),'--output',str(a.output/'dl-profile.txt')],a.output/'dl-run.log')
    coherence=run(a.robot_jar,['reason','--reasoner','hermit','--input',str(model),'--output',str(a.output/'classified.owl')],a.output/'coherence.log') if dl==0 else None
    # Functional checks exercise domain/range rather than merely read definitions.
    positive=flatten(schema);obs=URIRef('urn:provider:probe-observation');measurement=URIRef('urn:provider:probe-measurement')
    ports=URIRef(str(P)+'ports#hasMeasurement');feature=URIRef('urn:provider:probe-feature')
    positive.add((obs,ports,measurement));positive.add((obs,P.observedFor,feature))
    posfile=a.output/'domain-range-input.ttl';positive.serialize(posfile,format='turtle')
    code=run(a.robot_jar,['reason','--reasoner','hermit','--input',str(posfile),'--axiom-generators','ClassAssertion','--include-indirect','true','--output',str(a.output/'domain-range.owl')],a.output/'domain-range.log') if dl==0 else None
    inferred=Graph().parse(a.output/'domain-range.owl') if code==0 else Graph()
    entailments={'observation_domain':(obs,RDF.type,P.Observation) in inferred,'measurement_range':(measurement,RDF.type,P.Measurement) in inferred}
    # A datatype/property boundary breach must create an inconsistency through domain.
    negative=flatten(schema);negative.add((obs,P.observedFor,feature));negative.add((obs,RDF.type,P.MissingCell));nf=a.output/'negative-domain-input.ttl';negative.serialize(nf,format='turtle')
    neg=run(a.robot_jar,['reason','--reasoner','hermit','--input',str(nf),'--output',str(a.output/'negative-domain.owl')],a.output/'negative-domain.log') if dl==0 else None
    # BFO disjoint categories must make an injected class unsatisfiable.
    negative_class=flatten(schema);bad=URIRef('urn:provider:ImpossibleContinuantProcess');negative_class.add((bad,RDF.type,OWL.Class))
    for parent in ['BFO_0000002','BFO_0000003']:negative_class.add((bad,RDFS.subClassOf,URIRef('http://purl.obolibrary.org/obo/'+parent)))
    nf=a.output/'negative-bfo-input.ttl';negative_class.serialize(nf,format='turtle')
    negbfo=run(a.robot_jar,['reason','--reasoner','hermit','--input',str(nf),'--output',str(a.output/'negative-bfo.owl')],a.output/'negative-bfo.log') if dl==0 else None
    # Check expected errors, not just any process failure.
    rejected_domain=neg is not None and neg!=0 and 'INCONSISTENT' in (a.output/'negative-domain.log').read_text().upper()
    rejected_bfo=negbfo is not None and negbfo!=0 and 'UNSATISFIABLE' in (a.output/'negative-bfo.log').read_text().upper()
    report={'passed':dl==0 and coherence==0 and code==0 and all(entailments.values()) and rejected_domain and rejected_bfo,'model_manifest_sha256':sha(ROOT/'docs/current-release.json'),'lock':lock,'profile_DL_exit':dl,'hermit_coherence_exit':coherence,'domain_range_exit':code,'entailed':entailments,'negative_domain_rejected':rejected_domain,'negative_bfo_class_rejected':rejected_bfo,'scope':'All current PROVIDER modules + official BFO2020 core. Other referenced external terms are declarations only; no complete external PROV/SOSA/GeoSPARQL axiom closure. SHACL handles calendar datatype lexical constraints. Does not establish data truth, adequate granularity or partner approval.'}
    (a.output/'reasoning.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report));return 0 if report['passed'] else 1
if __name__=='__main__':raise SystemExit(main())
