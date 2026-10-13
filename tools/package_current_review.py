"""Package the current ontology candidate, executable questions and dated review."""
from pathlib import Path
import hashlib,json,zipfile
ROOT=Path(__file__).resolve().parents[1]
def main():
 r=ROOT;folder=r/'reports/ontology-review/2026-10-13';manifest=json.loads((r/'docs/current-release.json').read_text())
 names=[m['path'] for m in manifest['modules']]+[manifest['entry_point'],'ontology/current/catalog-v001.xml']+list(manifest['shape_hashes'])
 names += ['docs/current-release.json','docs/ontology-review.md','docs/dataset-coverage.json','docs/competency-questions.json','docs/competency-questions.md','examples/current/ap2-example.ttl','requirements-validation.txt','LICENSE','tools/review_current.py','tools/project_comext.py','tools/update_current_manifest.py','tools/build_ontology_review_report.py']
 names += [str(p.relative_to(r)) for p in (r/'queries/competency').glob('*.rq')]
 names += [str(p.relative_to(r)) for p in (r/'docs/review/2026-10-13').rglob('*') if p.is_file()]
 names += ['reports/ontology-review/2026-10-13/PROVIDER_Ontologie_Review.pdf']
 names=sorted(set(names));hashes={name:hashlib.sha256((r/name).read_bytes()).hexdigest() for name in names}
 info={'version':manifest['version'],'namespace':manifest['namespace'],'scope':'Current local ontology review candidate and discussion package; no raw Comext data, production migration or public approval','files':hashes,'regeneration':'Full checkout needed for historical tests; current review_current.py works from extracted package with requirements-validation environment. Comext adapter additionally needs provider-datasets and source bundle.'}
 readme='''# PROVIDER Ontologie-Review 13.10.2026

Zuerst reports/ontology-review/2026-10-13/PROVIDER_Ontologie_Review.pdf öffnen.
Aktuelles Modell: ontology/current/provider.ttl mit lokalem catalog-v001.xml.
Für die Offline-Prüfung Python-Umgebung aus requirements-validation.txt verwenden und aus dem Paketroot ausführen:

python tools/review_current.py --data examples/current/ap2-example.ttl --output output/review.json

Das Paket enthält den aktuellen Modellkandidaten, Kompetenzfragen, synthetische Beispiele und datierte Nachweise. Es enthält keine vollständigen echten Comext-Daten und nicht alle historischen Repositorydateien. Für historische Tests und die vollständige Git-Belegkette den Checkout verwenden. Keine öffentliche Datenfreigabe, keine Produktionsumschaltung und keine Partnerabnahme. Modullizenzen und Quelldatenbedingungen bleiben getrennt; insbesondere behält das Eventmodul seine CC-BY-4.0-Angabe.
'''
 target=folder/'PROVIDER_Ontologie_Review_Artefakte.zip'
 with zipfile.ZipFile(target,'w',compression=zipfile.ZIP_DEFLATED) as z:
  for name in names:
   entry=zipfile.ZipInfo(name,(2026,10,13,0,0,0));entry.compress_type=zipfile.ZIP_DEFLATED;z.writestr(entry,(r/name).read_bytes())
  for name,body in [('PAKET-LESEN.md',readme),('review-manifest.json',json.dumps(info,ensure_ascii=False,indent=2)+'\n')]:
   entry=zipfile.ZipInfo(name,(2026,10,13,0,0,0));entry.compress_type=zipfile.ZIP_DEFLATED;z.writestr(entry,body.encode())
 info['package']={'path':str(target.relative_to(r)),'sha256':hashlib.sha256(target.read_bytes()).hexdigest()}
 (folder/'artifact-manifest.json').write_text(json.dumps(info,ensure_ascii=False,indent=2)+'\n');print('Packaged',len(names),'hashed files')
if __name__=='__main__':main()
