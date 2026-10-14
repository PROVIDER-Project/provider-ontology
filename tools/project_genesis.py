"""Explicit canonical projection of reviewed, versioned GENESIS captures; no downloader."""
from __future__ import annotations
import argparse,csv,hashlib,json
from collections import Counter
from decimal import Decimal,InvalidOperation
from pathlib import Path
from rdflib import Graph,Namespace,URIRef,Literal
from rdflib.namespace import RDF,RDFS,XSD
from review_current import P,sha,validate_data,ROOT
DCT=Namespace('http://purl.org/dc/terms/');SKOS=Namespace('http://www.w3.org/2004/02/skos/core#')
BASE='https://projekt-provider.de/resource/genesis/'
SPECS=[('price-observations.csv','capture-manifest.json','61241-0006',P.PriceIndex),('production-observations.csv','production-capture-manifest.json','42153-0003',P.ProductionIndex),('gp9-publisher-observations.csv','gp9-publisher-manifest.json','42131-0002',None)]

def project(root:Path):
    folder=root/'catalog/ap21/genesis';g=Graph();proof=[];counts=Counter()
    for filename,manifest,table,index_kind in SPECS:
        path=folder/filename;meta_path=folder/manifest;meta=json.loads(meta_path.read_text());digest=sha(path)
        source=URIRef(BASE+'source/'+digest)
        for p,o in [(RDF.type,P.SourceRecord),(P.sourceHash,Literal(digest)),(P.sourceCheckedOn,Literal(meta['checked_on'],datatype=XSD.date)),(DCT.source,URIRef(meta['table_url'])),(DCT.license,URIRef(meta['license'])),(DCT.rights,Literal(meta['attribution']))]:g.add((source,p,o))
        # The hash binds the versioned projection, not unavailable original publisher bytes.
        g.add((source,RDFS.comment,Literal('Versioned capture/projection; current historical vintage, not original publication vintage. Exact acquisition timestamp unavailable.',lang='en')))
        stats=Counter()
        with path.open(newline='') as f:
            for row in csv.DictReader(f):
                period=row['period'];quarter='-Q' in period
                key=json.dumps([table,row['series_code'],period,row.get('production_scope',''),row.get('adjustment','')],ensure_ascii=False,separators=(',',':'))
                node=URIRef(BASE+'cell/'+hashlib.sha256(key.encode()).hexdigest())
                if (node,RDF.type,P.StatisticalCell) in g:raise ValueError('Duplicate cell key: '+key)
                concept=URIRef(BASE+'classification/'+row['series_code']);typ=P.EconomicActivityConcept if row['series_code'].startswith('WZ') else P.ProductClassificationConcept
                for p,o in [(RDF.type,P.ClassificationConcept),(RDF.type,typ),(SKOS.notation,Literal(row['series_code'])),(RDFS.label,Literal(row['label'],lang='de'))]:g.add((concept,p,o))
                token=row.get('source_value',row.get('value',''));numeric=row.get('numeric_value',token.replace('.','').replace(',','.')) if quarter else token.replace(',','.')
                marker=row.get('source_marker','')
                # A hyphen may be confidentiality-adjusted zero: never create an exact measured zero.
                missing=marker in ('.','-') or token in ('.','-','')
                value=None if missing else Decimal(numeric)
                if value is not None and not value.is_finite():raise ValueError('Non-finite value')
                for p,o in [(RDF.type,P.StatisticalCell),(RDF.type,P.MissingCell if missing else P.StatisticalObservation),(P.dataKind,Literal('real')),(P.presence,Literal('missing' if missing else 'explicit-zero' if value==0 else 'present')),(P.sourceRecord,source),(P.classificationConcept,concept),(P.observedFor,URIRef(BASE+'country/DE')),(P.sourceValue,Literal(token)),(P.providerStatus,Literal(marker or row.get('value_q',''))),(P.referenceQuarter if quarter else P.referenceMonth,Literal(period,datatype=XSD.string if quarter else XSD.gYearMonth))]:g.add((node,p,o))
                if marker and row.get('value_q'):g.add((node,P.providerStatus,Literal(row['value_q'])))
                for field,pred in [('production_scope',P.productionScope),('adjustment',P.adjustment)]:
                    if row.get(field):g.add((node,pred,Literal(row[field])))
                if not missing:
                    if index_kind:
                        kind=index_kind;unit=P['unit/IndexPoint']
                    else:
                        pair={'t':(P.ProductionMass,'Tonne'),'t-N':(P.NitrogenProductionMass,'TonneNitrogen'),'Stück':(P.ProductionCount,'Piece')}
                        if row['unit'] not in pair:raise ValueError('Unreviewed GP9 unit: '+row['unit'])
                        kind,u=pair[row['unit']];unit=P['unit/'+u]
                    measurement=URIRef(str(node)+'/measurement')
                    for p,o in [(RDF.type,P.StatisticalMeasurement),(P.measurementValue,Literal(value,datatype=XSD.decimal)),(P.measurementKind,kind),(P.hasUnit,unit)]:g.add((measurement,p,o))
                    g.add((node,P.hasMeasurement,measurement))
                    if index_kind:g.add((measurement,P.indexBase,Literal(row['value_unit'])))
                    stats['numeric']+=1
                else:stats['missing']+=1;stats['marker_'+marker]+=1
                stats['cells']+=1
        proof.append({'path':str(path.relative_to(root)),'sha256':digest,'manifest':str(meta_path.relative_to(root)),'manifest_sha256':sha(meta_path),'table':table,'counts':dict(stats),'source_hash_scope':'versioned derived capture; original publisher hash retained in original manifest, if available'})
        counts.update(stats)
    return g,{'sources':proof,'counts':dict(counts),'scope':'Bounded reviewed captures. No imputation, annual aggregation, plant-output inference, scheduled download, vintage reconstruction or production pipeline cutover.'}

def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--datasets-root',type=Path,required=True);parser.add_argument('--output',type=Path,required=True);a=parser.parse_args()
    model_pin=sha(ROOT/'docs/current-release.json')
    g,proof=project(a.datasets_root);a.output.parent.mkdir(parents=True,exist_ok=True)
    # Sorted N-Triples provide deterministic bytes (all data nodes have deterministic IRIs).
    a.output.write_text(''.join(sorted(g.serialize(format='nt').splitlines(keepends=True))))
    conforms,report=validate_data(g,profile='statistics');report.serialize(a.output.with_suffix('.shacl.ttl'),format='turtle')
    proof.update({'passed':conforms,'triples':len(g),'rdf_sha256':sha(a.output),'adapter_sha256':sha(Path(__file__)),'model_manifest_sha256':sha(ROOT/'docs/current-release.json')})
    if sha(ROOT/'docs/current-release.json')!=model_pin:raise ValueError('Model changed during validation; rerun')
    a.output.with_suffix('.json').write_text(json.dumps(proof,indent=2)+'\n');print(json.dumps({'passed':conforms,'counts':proof['counts']}));return 0 if conforms else 1
if __name__=='__main__':raise SystemExit(main())
