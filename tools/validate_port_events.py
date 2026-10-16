"""Offline validation of the optional coarse port-event profile and pinned rc3 base."""
import argparse,hashlib,json
from pathlib import Path
from rdflib import Graph
from pyshacl import validate
ROOT=Path(__file__).resolve().parents[1]
PROFILE=Path('profiles/port-events/0.1.0')

def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def load(root=ROOT):
    root=Path(root);folder=root/PROFILE;m=json.loads((folder/'manifest.json').read_text())
    if sha(root/'docs/current-release.json')!=m['base_manifest_sha256']:raise ValueError('Base manifest changed; explicit profile re-review required')
    g=Graph()
    for name,digest in {**m['base_files'],**{str(PROFILE/name):value for name,value in m['files'].items()}}.items():
        path=(root/name).resolve()
        if not path.is_relative_to(root.resolve()) or sha(path)!=digest:raise ValueError('Profile file pin changed: '+name)
        if name.endswith('.ttl') and not name.endswith('shapes.ttl'):g.parse(path)
    return m,g,Graph().parse(folder/'shapes.ttl')

def check(data,root=ROOT):
    m,model,shapes=load(root)
    passed,report,_=validate(data+model,shacl_graph=shapes,ont_graph=model,inference='none',meta_shacl=True,do_owl_imports=False)
    return bool(passed),report

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--data',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    g=Graph().parse(a.data);ok,report=check(g);a.output.mkdir(parents=True,exist_ok=True)
    report.serialize(a.output/'validation.ttl',format='turtle');(a.output/'result.json').write_text(json.dumps({'conforms':ok,'profile':'provider-port-events/0.1.0','input_sha256':sha(a.data),'profile_manifest_sha256':sha(ROOT/PROFILE/'manifest.json')},indent=2)+'\n')
    return 0 if ok else 1
if __name__=='__main__':raise SystemExit(main())
