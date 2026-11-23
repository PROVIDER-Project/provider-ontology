# PROVIDER isic4-cpc21

## Reproducible build

Run `make` or `make help` to list available goals.

- `make download`: download the original UNSD source into `target/resources/source.csv`.
- `make csv`: extract `target/isic4-cpc21.csv` using GDAL ogr2ogr.
- `make all` or `make all ENGINE=rpt`: generate `target/isic4-cpc21.ttl` with Docker RPT.
- `make all ENGINE=tarql`: generate RDF with Docker TARQL.
- `make clean` (or `make distclean`): remove the complete `target/` directory.

All downloads, extracted CSVs, temporary files and RDF outputs live under `target/`.
Dependencies: make, curl, GDAL (CSV/XLSX support), and Docker for RDF.
Leading zeroes and source partial/relationship indicators are preserved in CSV.
RDF emits simple `skos:closeMatch` edges, without those indicators.
Source URL: https://unstats.un.org/unsd/classifications/Econ/tables/CPC/CPCv21_ISIC4/cpc21-isic4.txt
Downloads are cached until `make clean`; the upstream URL is not version-pinned.

The BACI path is HS1992 → HS2017 → CPC2.1. Correspondences may be many-to-many;
they are candidate mappings, not allocation weights. Avoid summing trade values
across all matches without an allocation policy. `skos:closeMatch` is not transitive.
Namespaces use `https://data.projekt-provider.de/codes/` with `hs-1992/`,
`hs-2017/`, `hs-2012/`, `cpc-2.1/` and `isic-rev-4/` as applicable.
HS identifiers have six digits without dots. ISIC is at four-digit class level;
TiVA division mappings need an additional division-to-class hierarchy step.
