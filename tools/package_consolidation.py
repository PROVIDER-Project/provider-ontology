"""Package the dated candidate and hashed proof dossier, excluding actual source data."""
from pathlib import Path
import json,hashlib,zipfile
ROOT=Path(__file__).resolve().parents[1]
def main():
 r=ROOT;folder=r/'reports/ontology-review/2026-10-14';m=json.loads((r/'docs/current-release.json').read_text());assert m['version']=='0.3.0-rc2'
 proof=json.loads((r/'docs/review/2026-10-14/verification.json').read_text());assert proof['passed']
 names=[x['path'] for x in m['modules']]+list(m['shape_hashes'])+[x['entry_point'] for x in m['profiles'].values()]
 names += [m['entry_point'],'ontology/current/catalog-v001.xml','ontology/current/profiles/catalog-v001.xml','README.md','LICENSE','requirements-validation.txt','docs/current-release.json','docs/reasoner-lock.json','docs/ontology-consolidation.md','docs/model-profiles.md','docs/dataset-coverage.json','docs/competency-questions.json','docs/competency-questions.md','queries/common-measurements.rq','examples/current/ap2-example.ttl','examples/current/cppi-edition-description.ttl','reports/ontology-review/2026-10-14/PROVIDER_Ontologie_Konsolidierung.pdf']
 names += ['tools/'+name for name in ['review_current.py','update_current_manifest.py','audit_granularity.py','check_current_logic.py','fetch_reasoner.py','project_genesis.py','project_domain_pilots.py','project_comext.py','build_consolidation_report.py','package_consolidation.py']]
 names += [str(p.relative_to(r)) for p in (r/'queries/competency').glob('*.rq')]
 names += [str(p.relative_to(r)) for p in (r/'docs/review/2026-10-14').rglob('*') if p.is_file() and p.suffix!='.log']
 names=sorted(set(names));hashes={name:hashlib.sha256((r/name).read_bytes()).hexdigest() for name in names}
 info={'version':m['version'],'namespace':m['namespace'],'files':hashes,'model_manifest_sha256':hashlib.sha256((r/'docs/current-release.json').read_bytes()).hexdigest(),'scope':'Local candidate, model and reproducible acceptance dossier. No original real GENESIS/CPPI/GEM/Comext input files or full projected data. No production cutover or partner approval.'}
 readme='''# PROVIDER – Ontologie-Konsolidierung 14.10.2026

Bericht: reports/ontology-review/2026-10-14/PROVIDER_Ontologie_Konsolidierung.pdf.
Details: docs/ontology-consolidation.md; Fachprofile: docs/model-profiles.md.

Mit Python-Umgebung aus requirements-validation.txt ist die lokale Modellprüfung ohne Netzwerkimporte ausführbar:
python tools/review_current.py --data examples/current/ap2-example.ttl --output output/review.json

Die Java-Logikprüfung benötigt das separat hashgeprüfte ROBOT-JAR (tools/fetch_reasoner.py); BFO2020-Kern ist enthalten. Vollständige Repository-Regressionen benötigen den Checkout, zusätzliche Echtdatenpiloten die in der Dokumentation beschriebenen echten Inputs und provider-datasets. Dieses Paket enthält keine vollständigen echten Daten. Frühere rc1-Dateien sind als Vorgängerstand beigefügt. Lizenzen und Quellenbedingungen bleiben getrennt. Lokaler Kandidat, keine Veröffentlichung oder Partnerabnahme.
'''
 target=folder/'PROVIDER_Ontologie_Konsolidierung_Artefakte.zip'
 with zipfile.ZipFile(target,'w',compression=zipfile.ZIP_DEFLATED) as z:
  for name in names:
   entry=zipfile.ZipInfo(name,(2026,10,14,0,0,0));entry.compress_type=zipfile.ZIP_DEFLATED;z.writestr(entry,(r/name).read_bytes())
  z.writestr('PAKET-LESEN.md',readme);z.writestr('review-manifest.json',json.dumps(info,indent=2)+'\n')
 info['package_sha256']=hashlib.sha256(target.read_bytes()).hexdigest();(folder/'artifact-manifest.json').write_text(json.dumps(info,indent=2)+'\n');print('Packaged',len(names),'hashed files')
if __name__=='__main__':main()
