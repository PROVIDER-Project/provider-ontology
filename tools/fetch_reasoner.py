"""Fetch the explicitly pinned official ROBOT jar, verify bytes before saving."""
import argparse,json,hashlib,urllib.request
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',type=Path,required=True);a=p.parse_args();lock=json.loads((ROOT/'docs/reasoner-lock.json').read_text())['robot']
 with urllib.request.urlopen(lock['url'],timeout=60) as response:blob=response.read(128*1024*1024+1)
 if len(blob)>128*1024*1024 or hashlib.sha256(blob).hexdigest()!=lock['sha256']:raise ValueError('ROBOT download hash/size differs')
 if a.output.exists():raise ValueError('Choose a new path; preserve existing binary')
 a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_bytes(blob);print(lock['version'],lock['sha256'])
if __name__=='__main__':main()
