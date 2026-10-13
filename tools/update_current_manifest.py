"""Explicitly refresh release pins after reviewed edits; never called by validation."""
import argparse,hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--write',action='store_true',required=True);a=p.parse_args()
 path=ROOT/'docs/current-release.json';j=json.loads(path.read_text())
 def sha(name):return hashlib.sha256((ROOT/name).read_bytes()).hexdigest()
 for m in j['modules']:m['sha256']=sha(m['path'])
 j['entry_sha256']=sha(j['entry_point'])
 j['shape_hashes']={name:sha(name) for name in j['shape_hashes']}
 path.write_text(json.dumps(j,indent=2)+'\n')
if __name__=='__main__':main()
