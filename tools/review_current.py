"""Offline release checks, competency questions and profile-specific SHACL validation."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
from rdflib import Graph, URIRef, Namespace
from rdflib.namespace import RDF,RDFS,OWL
from pyshacl import validate

ROOT=Path(__file__).resolve().parents[1]
BASE='https://projekt-provider.de/ontology/'
P=Namespace(BASE)
SOSA=Namespace('http://www.w3.org/ns/sosa/')


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def member(root,name):
    path=Path(root)/name
    if path.is_symlink() or not path.resolve().is_relative_to(Path(root).resolve()):
        raise ValueError('Unsafe release path: '+name)
    return path


def load(root=ROOT, profile="all"):
    root=Path(root);manifest=json.loads((root/'docs/current-release.json').read_text())
    if manifest['namespace']!=BASE:raise ValueError('Unexpected active namespace')
    graph=Graph()
    iris={m['ontology_iri'] for m in manifest['modules']}
    for item in manifest['modules']:
        path=member(root,item['path'])
        if sha(path)!=item['sha256']:raise ValueError('Changed module: '+item['path'])
        module=Graph().parse(path,format='turtle')
        if set(module.subjects(RDF.type,OWL.Ontology))!={URIRef(item['ontology_iri'])}:raise ValueError('Module header mismatch')
        if {str(v) for v in module.objects(None,OWL.imports)}-iris:raise ValueError('Unresolved local import: '+item['path'])
        graph+=module
    entry=member(root,manifest['entry_point'])
    if sha(entry)!=manifest['entry_sha256']:raise ValueError('Changed entry point')
    for path,expected in manifest['shape_hashes'].items():
        if sha(member(root,path))!=expected:raise ValueError('Changed shape: '+path)
    for descriptor in manifest['profiles'].values():
        if sha(member(root,descriptor['entry_point']))!=descriptor['sha256']:
            raise ValueError('Changed profile entry point')
    if profile not in manifest['profiles']:
        raise ValueError('Unknown model profile: '+profile)
    descriptor=manifest['profiles'][profile]
    entry_graph=Graph().parse(member(root,descriptor['entry_point']),format='turtle')
    if sha(member(root,descriptor['entry_point']))!=descriptor['sha256']:
        raise ValueError('Changed profile entry point: '+profile)
    modules={item['ontology_iri']:item for item in manifest['modules']}
    pending=[str(iri) for iri in entry_graph.objects(None,OWL.imports)];selected=set()
    while pending:
        iri=pending.pop()
        if iri in selected:continue
        if iri not in modules:raise ValueError('Unresolved profile import: '+iri)
        selected.add(iri)
        module=Graph().parse(member(root,modules[iri]['path']),format='turtle')
        pending.extend(str(v) for v in module.objects(None,OWL.imports))
    if profile!='all':
        graph=Graph()
        for iri in sorted(selected):graph.parse(member(root,modules[iri]['path']),format='turtle')
    return manifest,graph


def ancestors(graph,cls):
    found={cls};stack=[cls]
    while stack:
        for parent in graph.objects(stack.pop(),RDFS.subClassOf):
            if isinstance(parent,URIRef) and parent not in found:found.add(parent);stack.append(parent)
    return found


def audit(root=ROOT):
    manifest,g=load(root);errors=[]
    properties=set(g.subjects(RDF.type,OWL.ObjectProperty))&set(g.subjects(RDF.type,OWL.DatatypeProperty))
    if properties:errors.append('Object/datatype property collision: '+str(sorted(properties)))
    forbidden=('http://projekt-provider.de/ontology/','https://provider-projekt.de/ontology/','https://w3id.org/provider/ontology/')
    if any(isinstance(n,URIRef) and str(n).startswith(forbidden) for t in g for n in t):errors.append('Legacy model namespace in active graph')
    for cls in set(g.subjects(RDF.type,OWL.Class)):
        supers=ancestors(g,cls)
        if P.Observation in supers and SOSA.Observation in supers:errors.append('Result/activity collision: '+str(cls))
        if P.Commodity in supers and P.CommodityConcept in supers:errors.append('Physical/concept collision: '+str(cls))
    for predicate in set(g.subjects(RDFS.subPropertyOf,SOSA.hasFeatureOfInterest)):
        if any(P.Observation in ancestors(g,domain) for domain in g.objects(predicate,RDFS.domain)):
            errors.append('Result property implies SOSA activity: '+str(predicate))
    local_classes={s for s in g.subjects(RDF.type,OWL.Class) if str(s).startswith(BASE)}
    unlabeled=sorted(str(s) for s in local_classes if not list(g.objects(s,RDFS.label)))
    if unlabeled:errors.append('Unlabeled local classes: '+str(unlabeled))
    modules=[{'path':x['path'],'sha256':x['sha256']} for x in manifest['modules']]
    return {'passed':not errors,'namespace':BASE,'version':manifest['version'],'modules':modules,
            'triples':len(g),'classes':len(local_classes),'errors':errors,
            'scope':'Offline structural and explicit hierarchy checks; not complete OWL2 DL, complete BFO import closure or production release approval.'}


def validate_data(data,*,root=ROOT,profile='statistics',meta=True):
    manifest,schema=load(root)
    if profile not in manifest['shapes']:raise ValueError('Unknown validation profile')
    shapes=Graph()
    for name in manifest['shapes'][profile]:shapes.parse(member(root,name),format='turtle')
    if not len(data):raise ValueError('Empty data graph is not an acceptance test')
    # Explicit schema and controlled vocabulary individuals are available to SPARQL.
    # No domain/range or OWL inference is used, and caller data remain untouched.
    validation_input=data+schema
    conforms,report,_=validate(validation_input,shacl_graph=shapes,ont_graph=schema,inference='none',
        meta_shacl=meta,advanced=False,do_owl_imports=False,inplace=False,js=False)
    if not isinstance(report,Graph):raise ValueError('SHACL execution did not return a graph')
    return bool(conforms),report


def competency_questions(root=ROOT):
    root=Path(root);_,schema=load(root);data=Graph().parse(root/'examples/current/ap2-example.ttl')
    graph=schema+data;results=[]
    for cq in json.loads((root/'docs/competency-questions.json').read_text())['questions']:
        query=member(root,cq['query']).read_text();result=graph.query(query)
        if result.type=='ASK':actual=bool(result.askAnswer)
        else:actual=sorted([['' if v is None else str(v) for v in row] for row in result])
        results.append({'id':cq['id'],'passed':actual==cq['expected'],'actual':actual,'expected':cq['expected']})
    return results


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--root',type=Path,default=ROOT)
    p.add_argument('--data',type=Path);p.add_argument('--profile',default='statistics');p.add_argument('--output',type=Path,required=True)
    a=p.parse_args();report=audit(a.root)
    report['competency_questions']=competency_questions(a.root)
    report['passed'] &= all(x['passed'] for x in report['competency_questions'])
    if a.data:
        data=Graph().parse(a.data);passed,shacl=validate_data(data,root=a.root,profile=a.profile)
        report['shacl']={'conforms':passed,'profile':a.profile,'input_sha256':sha(a.data)};report['passed'] &= passed
        a.output.parent.mkdir(parents=True,exist_ok=True);shacl.serialize(a.output.with_suffix('.shacl.ttl'),format='turtle')
    a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({'passed':report['passed'],'modules':len(report['modules']),'competency_questions':len(report['competency_questions'])}))
    return 0 if report['passed'] else 1

if __name__=='__main__':raise SystemExit(main())
