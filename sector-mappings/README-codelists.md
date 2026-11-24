# Code lists at a glance

| Code list | Classifies | Remember it as | Project |
|---|---|---|---|
| **ISIC Rev. 4** | Economic activities / industries, including services | What a business **does** | [isic4](isic4/) |
| **CPC 2.1** | Products: goods **and services** | What a business **produces or supplies** | [cpc21](cpc21/) |
| **HS 1992** (1988/1992) | Traded goods / commodities | What crosses borders — the edition used by our BACI 1995 data | [hs1992](hs1992/) |
| **HS 2017** | Traded goods / commodities | What crosses borders — a newer edition | [hs2017](hs2017/) |

ISIC = International Standard Industrial Classification of All Economic Activities;
CPC = Central Product Classification; HS = Harmonized System.
HS covers goods, not services. HS1992 and HS2017 are editions of the same classification.

## Building

Run these commands inside the individual project directory:

- `make` or `make help`: show available goals.
- `make download`: download the official source into `target/resources/`.
- `make csv`: download and extract the code list into `target/`.
- `make all`: generate RDF using Docker RPT.
- `make all ENGINE=tarql`: generate RDF using Docker TARQL.
- `make clean`: remove all downloaded and generated files under `target/`.

The RDF uses the same PROVIDER code IRIs as the mappings, with English labels,
code notations, concept schemes and hierarchy links. See each project's README
for official source URLs, dependencies and coverage details, including Comtrade's
special/legacy entries and CPC's unexpanded trade-service templates.
