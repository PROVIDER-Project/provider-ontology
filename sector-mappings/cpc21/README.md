# CPC Version 2.1 code list

Official source: https://unstats.un.org/unsd/classifications/Econ/Download/In%20Text/CPC_Ver_2.1_Exp_Notes_Updated_3Apr2025.xlsx

`make` / `make help` lists goals. `make download` caches the source under
`target/resources/`. `make csv` produces `target/cpc21.csv` (code, label,
parent). `make all` produces `target/cpc21.ttl` using Docker RPT;
`make all ENGINE=tarql` uses Docker TARQL. `make clean` / `make distclean`
removes all of `target/`. Requires curl, Python 3, Docker for RDF,
and GDAL ogr2ogr for CPC Excel extraction. No Python packages are needed.

All generated and downloaded files stay in `target/`. Downloads are cached;
clean to refresh. Upstream URLs are not content-pinned. Codes remain strings,
including leading zeroes. Extraction rejects duplicate codes and missing
parents or labels. RDF uses English skos:prefLabel, skos:notation,
skos:inScheme, skos:broader and top-concept links.
Namespace: `https://data.projekt-provider.de/codes/cpc-2.1/`.
Scheme: `https://data.projekt-provider.de/codes/cpc-2.1/scheme`.

The CPC2.1 worksheet supplies all explicit codes and titles. Its header row
is excluded. The 61_62 sheet contains templates (*** placeholders) for trade
services; these are not expanded into invented code combinations. See the
workbook Notes sheet: applicability varies. Thus this build does not claim
an expanded enumeration of those template-based trade-service subdivisions.
The downloaded workbook preserves explanatory notes and all other sheets;
only titles and hierarchy are emitted in RDF.
