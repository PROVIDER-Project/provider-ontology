# HS 1988/1992 code list

Official source: https://comtradeapi.un.org/files/v1/app/reference/H0.json

`make` / `make help` lists goals. `make download` caches the source under
`target/resources/`. `make csv` produces `target/hs1992.csv` (code, label,
parent). `make all` produces `target/hs1992.ttl` using Docker RPT;
`make all ENGINE=tarql` uses Docker TARQL. `make clean` / `make distclean`
removes all of `target/`. Requires curl, Python 3, Docker for RDF,
and GDAL ogr2ogr for CPC Excel extraction. No Python packages are needed.

All generated and downloaded files stay in `target/`. Downloads are cached;
clean to refresh. Upstream URLs are not content-pinned. Codes remain strings,
including leading zeroes. Extraction rejects duplicate codes and missing
parents or labels. RDF uses English skos:prefLabel, skos:notation,
skos:inScheme, skos:broader and top-concept links.
Namespace: `https://data.projekt-provider.de/codes/hs-1992/`.
Scheme: `https://data.projekt-provider.de/codes/hs-1992/scheme`.

All Comtrade reference entries are retained, including TOTAL, aggregates,
special and legacy non-WCO codes. These are UN Comtrade labels, not a claim
that every entry is a standard WCO six-digit code. The code prefix is removed
from labels where present. Some HS92 labels depend on their parent context.
