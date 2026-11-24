# ISIC Revision 4 code list

Official source: https://unstats.un.org/unsd/classifications/Econ/Download/In%20Text/ISIC_Rev_4_english_structure.Txt

`make` / `make help` lists goals. `make download` caches the source under
`target/resources/`. `make csv` produces `target/isic4.csv` (code, label,
parent). `make all` produces `target/isic4.ttl` using Docker RPT;
`make all ENGINE=tarql` uses Docker TARQL. `make clean` / `make distclean`
removes all of `target/`. Requires curl, Python 3, Docker for RDF,
and GDAL ogr2ogr for CPC Excel extraction. No Python packages are needed.

All generated and downloaded files stay in `target/`. Downloads are cached;
clean to refresh. Upstream URLs are not content-pinned. Codes remain strings,
including leading zeroes. Extraction rejects duplicate codes and missing
parents or labels. RDF uses English skos:prefLabel, skos:notation,
skos:inScheme, skos:broader and top-concept links.
Namespace: `https://data.projekt-provider.de/codes/isic-rev-4/`.
Scheme: `https://data.projekt-provider.de/codes/isic-rev-4/scheme`.

The source is CSV despite its .Txt URL. Section parents of divisions follow
the official row order; group/class parents follow code prefixes. All levels
are retained, including sections and the divisions used by TiVA.
