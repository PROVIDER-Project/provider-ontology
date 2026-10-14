"""Enumerate local terms and evidence, resolving SPARQL prefix names as well as full IRIs."""
import argparse,json,collections,re,hashlib
from pathlib import Path
from rdflib import Graph,URIRef
from rdflib.namespace import RDF,RDFS,OWL
BASE='https://projekt-provider.de/ontology/'
TYPES=(OWL.Class,OWL.ObjectProperty,OWL.DatatypeProperty,OWL.AnnotationProperty)

def question_terms(text):
    prefixes=dict(re.findall(r'(?i)PREFIX\s+([\w-]*):\s*<([^>]+)>',text))
    iris=set(re.findall(r'<([^>]+)>',text))
    for prefix,local in re.findall(r'(?<![\w/])([\w-]*):([\w-]+)',text):
        if prefix in prefixes:iris.add(prefixes[prefix]+local)
    return iris

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1]);p.add_argument('--model-root',type=Path);p.add_argument('--output',type=Path,required=True);a=p.parse_args();model=a.model_root or a.root
    manifest=json.loads((model/'docs/current-release.json').read_text());modules={m['path']:Graph().parse(model/m['path']) for m in manifest['modules']};g=Graph()
    for module in modules.values():g+=module
    fixture=Graph().parse(a.root/'examples/current/ap2-example.ttl');fixture_terms={str(n) for t in fixture for n in t if isinstance(n,URIRef)}
    questions=json.loads((a.root/'docs/competency-questions.json').read_text())['questions'];qterms={q['id']:question_terms((a.root/q['query']).read_text()) for q in questions};coverage=json.loads((a.root/'docs/dataset-coverage.json').read_text())['sources'];terms=[]
    for term in sorted({s for typ in TYPES for s in g.subjects(RDF.type,typ) if str(s).startswith(BASE)},key=str):
        used=str(term) in fixture_terms;cqs=[key for key,iris in qterms.items() if str(term) in iris];sources=[s['source_id'] for s in coverage if str(term) in s['model_terms']];deprecated=any(str(v).lower()=='true' for v in g.objects(term,OWL.deprecated))
        category='deprecated-compatibility' if deprecated else 'exercised-model' if used or cqs else 'source-mapped-not-exercised' if sources else 'extension-not-exercised'
        terms.append({'iri':str(term),'types':sorted(str(v) for v in g.objects(term,RDF.type) if v in TYPES),'declared_in':[name for name,module in modules.items() if any((term,RDF.type,typ) in module for typ in TYPES)],'category':category,'fixture_used':used,'competency_questions':cqs,'source_mappings':sources,'decision':'retain; compatibility only' if deprecated else 'retain; exercised in acceptance examples' if used or cqs else 'retain in optional/domain module; empirical use not established','domains':sorted(map(str,g.objects(term,RDFS.domain))),'ranges':sorted(map(str,g.objects(term,RDFS.range)))})
    report={'version':manifest['version'],'manifest_sha256':hashlib.sha256((model/'docs/current-release.json').read_bytes()).hexdigest(),'scope':'All declared local classes/properties. Resolved SPARQL prefixes. Usage evidence is not redundancy proof. Synthetic fixture coverage does not establish real integration.','counts':dict(collections.Counter(t['category'] for t in terms)),'terms':terms}
    a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report['counts']))
if __name__=='__main__':main()
