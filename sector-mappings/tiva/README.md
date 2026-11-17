# TIVA → ISIC Rev. 4 Sector Mappings

RDF-ization of the TIVA (Technology-Induced Value Added) sector classification —
economic activities and industry aggregates — and its mappings to ISIC
Revision 4.

## Source

The data was extracted from **pages 46–47** of the OECD
[TiVA 2025 Indicators Guide](https://webfs-sti.oecd.org/files/STI-PIE/TIVA/2025/TiVA_2025_Indicators_Guide.pdf).
Local copies of the source material live in [`tmp/`](tmp/):

- `TiVA_2025_Indicators_Guide.pdf` — the full guide
- `page46.pdf`, `page47.pdf` — the extracted pages with the sector tables

The work is tracked in
[PROVIDER-Project/sparql-tiva-ontop#1 — Add mappings from Tiva to ISIC Rev.4](https://github.com/PROVIDER-Project/sparql-tiva-ontop/issues/1).

## Files

| File | Content |
|---|---|
| `sectors.csv` / `sectors.tarql.rq` | 50 TIVA activities: code, English label, and the ISIC Rev. 4 section it belongs to (section-level codes `A`–`T` and 2-digit codes such as `A01`). |
| `code-to-isicrev4.csv` / `code-to-isicrev4.tarql.rq` | 94 rows: each TIVA sector code mapped to the ISIC Rev. 4 2-digit (division) code(s) it covers. |
| `industry-aggregate-code-to-isicrev4divisions.csv` / `…tarql.rq` | 411 rows: each TIVA industry-aggregate code mapped to the ISIC Rev. 4 divisions it aggregates (e.g. range aggregates like `A01T02`). |
| `industry-aggregate-labels.csv` / `industry-aggregate-labels.tarql.rq` | 30 industry aggregates with English labels (e.g. `GTT` "Total Services (excl. construction)", `JTN`, `INFO`, `_T` = TOTAL). |
| `Makefile` | Generates the RDF (see below). |
| `target/` | Generated Turtle output (one `.ttl` per CSV). |
| `tmp/` | Source PDFs (see above). |

The TIVA codes used here: sections `A`–`T`, 2-digit activity codes such as
`A01`, range aggregates such as `A01T02` ("from A01 to A02"), and the named
aggregates listed in `industry-aggregate-labels.csv`.

## RDF design

Each CSV has a matching TARQL `CONSTRUCT` query that mints `skos:Concept`
instances:

- **TIVA activities and aggregates** are `skos:Concept`s in the concept
  scheme `https://data.projekt-provider.de/tiva/scheme/activity`, with
  `skos:notation` (the code) and `skos:prefLabel` (`@en`). Data IRIs are of
  the form `https://data.projekt-provider.de/tiva/activity/<code>`.
- **Mappings to ISIC Rev. 4** use properties from the TIVA schema
  (`https://schema.projekt-provider.de/tiva#`): `tivao:isicRev4Section`,
  `tivao:isicRev4Code`, and `tivao:isicRev4Division`.
- **ISIC Rev. 4 codes** are `skos:Concept`s in the scheme
  `https://data.projekt-provider.de/codes/isic-rev-4/scheme` ("ISIC Revision 4"),
  with IRIs of the form `https://data.projekt-provider.de/codes/isic-rev-4/<code>`.

## Generating the RDF

The `Makefile` runs the TARQL queries through Docker and writes one Turtle
file per CSV into `target/`:

```sh
make              # generate all target/*.ttl with RPT (default engine)
make ENGINE=tarql # use the original mikulas/tarql image instead
make clean        # remove generated RDF files
```

- `ENGINE=rpt` (default): `aksw/rpt:2.0.0-rc7`, `sansa tarql`, Turtle/blocks output
- `ENGINE=tarql`: `mikulas/tarql` with UTF-8 input

Both require Docker; each run mounts this directory into the container as
`/data`.
