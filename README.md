# PROVIDER Ontology

## Aktueller Modellstand

**Zielnamensraum: `https://projekt-provider.de/ontology/`.**

Der lokale Reviewkandidat **0.3.0-rc3** liegt ausschließlich unter [`ontology/current/`](ontology/current/). Schlanke Einstiege: [`Fachprofile`](docs/model-profiles.md); vollständige Gesamtprüfung: [`provider.ttl`](ontology/current/provider.ttl). Das [Release-Manifest](docs/current-release.json) bindet 17 Module, Imports und Validierungsprofile an konkrete Dateihashes. Der lokale XML-Katalog neben den Modulen ordnet Ontologie- und Versions-IRIs den Dateien zu. Die Website muss dafür nicht veröffentlicht sein; unsere Prüftools laden die Manifestdateien offline.

[Konsolidierungsbasis rc2 und Echtdatenabnahme](docs/ontology-consolidation.md) · [Fachprofile](docs/model-profiles.md) · [Vorheriger Review](docs/ontology-review.md) · [Kompetenzfragen](docs/competency-questions.md) · [Abdeckung aller 34 Registereinträge](docs/dataset-coverage.json)

| Modul | Zweck |
|---|---|
| `core.ttl`, `bfo-alignment.ttl` | Gemeinsame Organisationen, Anlagen, Produkte, Prozesse, Ergebnisse und Evidenz |
| `statistics.ttl` | Statistische Zellen, Datenlücken, Einheiten, Klassifikationen und Zeitbezüge |
| `ports.ttl`, `infrastructure.ttl`, `network.ttl` | Häfen, Ortscodes, Flächen, Infrastruktur und routebezogene Reihenfolge |
| `cppi.ttl`, `cppi-source.ttl` | Jahresbeobachtungen, Scores und explizite Quellenbindung |
| `mining*.ttl` | Minen, Komplexe, Materialien, Ergebnisse und qualifizierte Zuordnungen |
| `event.ttl` | Ereignisse, Gefahren, Konflikte und Exposition; kein automatischer Ausfallnachweis |
| `supply-chain.ttl`, `source-alignment.ttl` | Lieferkettenoperationen und begrenzte Quellenausrichtungen |

Aktuelle Ergänzung: [Transportprofil rc3](docs/transport-network.md), mit getrennter physischer Infrastruktur, Topologie und berechneten Sperrszenarien.

## Prüfen

Validierungsumgebung mit `requirements-validation.txt` einrichten. Dann:

```sh
python -m unittest discover -s tests -v
python tools/review_current.py --data examples/current/ap2-example.ttl --output output/current-review.json
```

Das synthetische Gesamtbeispiel und 34 SPARQL-Kompetenzfragen prüfen Modellierbarkeit und semantische Grenzen. Das ist keine Bestätigung empirischer Vollständigkeit oder Partnerabnahme. OWL beschreibt Bedeutung; SHACL prüft die angegebenen Datenprofile ohne Domain-/Range-Inferenz und ohne Netzwerkimports.

## Comext gegen das gemeinsame Modell prüfen

Bei installiertem aktuellem `provider-datasets` oder dessen `src/` im Python-Pfad:

```sh
PYTHONPATH=../provider-datasets/src python tools/project_comext.py --bundle ../provider-datasets/output/comext/2026-10-13 --output output/comext-provider.nt --validate
```

Die Projektion erzeugt neue kanonische Ergebnisressourcen und verändert den Quellgraphen nicht. Eingangsmanifest, Quellenhinweise, Datentypen, Datenlücken und Jahreszuordnungen bleiben nachvollziehbar. Bestehende Ausgaben werden nicht überschrieben. Andere produktive Quelladapter und die Workflow-Pins müssen separat auf die neue Modellversion migriert und geprüft werden.

## Historische Baselines und lokale Entwürfe

Die bisherigen Dateien direkt unter `ontology/`, `shapes/`, die alten AP2-Manifeste und Beispiele bleiben unverändert für die bereits gepinnten Workflow-/Dataset-Versionen erhalten. Sie sind **kein zweiter aktueller Modellstand**. Insbesondere ist `ontology/provider-main.xml` kein aktueller Export. Alte und neue Ontologien nicht unkontrolliert gemeinsam laden.

Die lokalen Entwürfe `provider-main.ttl` im Root und `ontology/provider-event.ttl` wurden gelesen und unter `docs/review/2026-10-13/inputs/` unverändert gesichert. Die Originale bleiben unangetastet. Ihre Übernahmeentscheidungen und Einschränkungen stehen im Review.

## Versionierung, Bedingungen und Grenzen

Das ist ein lokal getesteter Reviewkandidat, keine öffentliche Veröffentlichung. Hashes nach bewusster fachlicher Änderung über `tools/update_current_manifest.py --write` aktualisieren und alle Prüfungen wiederholen. Die Module behalten ihre Lizenzangaben: der übernommene Event-Entwurf nennt CC BY 4.0, weitere Module MIT. Datenlizenzen und die Bedingungen externer Vokabulare werden dadurch nicht ersetzt.

[Repository-Zuordnung](docs/repositories.md) · [Historische AP2-Profilbeschreibung](docs/ap2-pilot-profile.md)
