# PROVIDER: Ontologie-Review und konsolidiertes Modell

Stand 13.10.2026. Reviewkandidat **0.3.0-rc1**, Zielnamensraum **https://projekt-provider.de/ontology/**.

## Ergebnis

Der aktive Modellstand ist jetzt über `ontology/current/provider.ttl` und `docs/current-release.json` eindeutig bestimmt. 15 gehashte Module decken Core, Lieferkettenoperationen, Infrastruktur/Netze, Häfen, CPPI, Mining, Ereignisse und statistische Ergebnisse ab. 31 ausführbare Kompetenzfragen zeigen Modellierbarkeit und Grenzen mit ausdrücklich synthetischen Beispielen. Alle 34 Einträge des derzeitigen Datasetregisters sind im Modell-Coverage-Dossier zugeordnet. Ausgewählt bedeutet weder bereits integriert noch öffentlich freigegeben.

Die bisherigen gepinnten Baselines bleiben unverändert, damit bestehende Dataset- und Workflowartefakte überprüfbar bleiben. Sie sind historische Abnahmen und dürfen nicht unkontrolliert mit dem aktuellen Schema vereinigt werden. Die beiden lokalen Entwürfe sind unverändert als Revieweingänge gesichert; ihre Originale wurden nicht editiert oder automatisch committed.

## Methode und Bestandsumfang

32 vorhandene RDF-Dateien einschließlich Shapes, Beispiele, des älteren RDF/XML und beider lokaler Entwürfe wurden syntaktisch inventarisiert. Alle waren parsebar. Der Rootentwurf0.1 bietet keine zusätzlichen Klassen gegenüber dem bisherigen Core0.2; seine direkte gistBFO-Importierung wurde nicht ungeprüft übernommen. Das Eventmodul wurde in die neue Modulstruktur überführt und fachlich an den Core angebunden.

Das Review prüft Identifikatoren und Versionen, Imports, Klassen-/Propertyrollen, Ergebnis/Aktivität, physische Entität/Konzept, Zeitbezüge, Einheiten, Missingness, Herkunft, qualifizierte Aussagen und Modellabdeckung. OWL beschreibt Bedeutungsbeziehungen und ersetzt keine Datenvollständigkeitsprüfung; SHACL überprüft die konkreten Datenprofile. Siehe [OWL2 Primer](https://www.w3.org/TR/owl2-primer/), [SHACL](https://www.w3.org/TR/shacl/) und für die Comext-Quellrepräsentation [RDF Data Cube](https://www.w3.org/TR/vocab-data-cube/). Die neue Statistikprojektion beansprucht keine vollständige Data-Cube-Konformität.

## Befunde und Entscheidungen

### R01 · P0 · Uneinheitliche Modellnamensräume

Status: `resolved`. Aktiver Reviewkandidat verwendet ausschließlich https://projekt-provider.de/ontology/ mit nachvollziehbaren Modulnamensräumen. HTTP, provider-projekt.de und w3id-Entwürfe sind aus dem aktiven Schema entfernt; keine pauschale Instanzumschreibung.

### R02 · P0 · Mehrere scheinbar aktuelle Core-Dateien

Status: `resolved`. Ein aktiver Einstieg und gehashtes Manifest. Rootentwurf0.1 enthält keine zusätzlichen Klassen gegenüber dem bisherigen Core0.2 und ersetzt ihn nicht. XML und alte Profile sind ausdrücklich historisch.

### R03 · P0 · Physische Waren und Klassifikationsbegriffe vermischt

Status: `resolved`. Commodity/Material beschreiben physische Produkte; CommodityConcept/MaterialConcept und CNSelection beschreiben Begriffe. Mining verweist bei Warenarten auf Konzepte. Keine globale Gleichsetzung mit HS2017.

### R04 · P0 · Beobachtungsergebnis kann als Aktivität typisiert werden

Status: `resolved`. Mining-Ergebnis und SOSA-Aktivität sind getrennt. Ergebnisprädikate erzwingen keine SOSA-Aktivitätsklasse. Neue Prüfregeln erkennen die Vermischung.

### R05 · P0 · Gefahr impliziert automatisch Lieferkettenausfall

Status: `resolved`. HazardEvent ist ein Ereignis, kein automatisch realisierter DisruptionEvent. Exposition, qualifizierte Wirkungsaussage und Szenarioannahme bleiben getrennt.

### R06 · P1 · Fehlende Statistikgrundlage für Comext und GENESIS

Status: `resolved`. Gemeinsames Profil für fehlende Zellen, Werte, Einheiten, Kennzahlarten, Monats-/Quartals-/Jahres-/Saisonbezug und Klassifikationsrevision. Vollständige Jahressummen getrennt von Teilsummen.

### R07 · P1 · Routeposition als globale Segmenteigenschaft

Status: `resolved`. RouteStep bindet Segment und Position an eine konkrete Route. Derselbe Abschnitt kann in mehreren Routen verschiedene Positionen haben. Berechnete Route ist keine beobachtete Fahrt.

### R08 · P1 · Fehlende überprüfbare Kompetenzfragen und Quellenabdeckung

Status: `resolved`. 31 ausführbare SPARQL-Fragen plus synthetisches Gesamtbeispiel. Alle34 Registereinträge einschließlich zurückgestellter Quellen haben explizite Modell- und Migrationszuordnung.

### R09 · P1 · Produktive Producer und Workflow-Pins nutzen ältere Profile

Status: `open-production-migration`. Comext besitzt einen expliziten, real geprüften Adapter. Ports, CPPI, Mining, GDACS, Soja, OSM und Routing benötigen getrennt versionierte Adapter-/Pin-Migrationen. Bestehende Artefakte und historische Tests wurden nicht rückwirkend umgedeutet.

### R10 · P1 · Vollständige externe BFO-/OWL2-DL-Prüfung fehlt

Status: `bounded-validation`. Lokale Struktur-, SHACL- und Kompetenzprüfungen sowie ein OWL-RL-Smoke-Test sind möglich. Keine vollständige externe Importclosure, keine vollständige OWL2-DL-Konsistenzzertifizierung und keine Partnerabnahme behauptet.

### R11 · P1 · Kompetenzfragen sind noch nicht gemeinsam abgenommen

Status: `open-partner-review`. Fragen decken bestehende Arbeitsanforderungen ab; AP1 und Modellpartner müssen Relevanz, Umfang und fachliche Definitionen bestätigen. Kein Versand oder erfundene Zustimmung.

### R12 · P2 · Namespace allein veröffentlicht die Ontologie nicht

Status: `open-publication`. Lokaler XML-Importkatalog und Releasepins sind vorhanden. Websiteauflösung, HTTP-Weiterleitungen, Content Negotiation, öffentliche Versionen und Produktionsumschaltung sind eigene Veröffentlichungsschritte.

## Verbindliche Modellregeln

- Organisation, physische Anlage, Ortscode, Geometrie, Quelle und Szenariorepräsentation sind getrennte Ressourcen.
- Commodity/Material sind physische Waren; Klassifikationen und Warenauswahlgruppen sind Konzepte. Ein Code belegt weder konkrete Ladung noch Firma.
- Beobachtungsergebnis, Beobachtungsaktivität und Datenabruf sind verschieden. Source-SOSA-Typen werden nicht pauschal zu kanonischen Ergebnissen.
- Monats-, Quartals-, Jahres- und Ernteperioden bleiben erhalten. Beobachtungszeit, Provider-Update, Veröffentlichung, Gültigkeit und Abruf sind getrennte Angaben; unbekannte Zeiten werden nicht erfunden.
- Handelsmasse, Produktionsmasse, Stickstoffmenge, Kapazität, Index, Rang und Anteil haben unterschiedliche Kennzahlarten und kontrollierte Einheiten. t-N bezeichnet enthaltenen Stickstoff, nicht die Warenmasse. Preis-/Produktionsindex benötigt eine Basis; negative CPPI-/SPI-Werte bleiben gültig.
- Fehlend ist kein Nullwert und kein Ausfall. Eine beobachtete Teilsumme ist kein vollständiges Jahr. Providerkennzeichen bleiben Quellenkennzeichen ohne unbelegte Ursacheninterpretation.
- Gefahr, Exposition, vermutete Wirkung und belegter Ausfall werden nicht gleichgesetzt. Geplante und angenommene Aussagen bleiben qualifiziert und werden nicht als empirische Tripel materialisiert.
- Quellen-/Codebedingungen, Bearbeitungshinweise und Publikationsentscheidungen sind getrennt. Das Eventmodul behält CC BY4.0, andere Module ihre MIT-Angaben; daraus folgt keine Datenlizenz oder Lizenzfreigabe für den gesamten KG.

## Nachweise und Bedienung

`docs/competency-questions.md` verlinkt alle31 ausführbaren Fragen. `docs/dataset-coverage.json` nennt für jeden Registereintrag Begriffe, Kompetenzfragen, Arbeitsanforderungen und Adapterstatus. `docs/review/2026-10-13/` enthält Bestandsaufnahme, Entwurfvergleich, Migrationsentscheidungen und aktuelle Laufnachweise.

```sh
python -m unittest discover -s tests -v
python tools/review_current.py --data examples/current/ap2-example.ttl --output output/current-review.json
PYTHONPATH=../provider-datasets/src python tools/project_comext.py --bundle ../provider-datasets/output/comext/2026-10-13 --output output/comext-provider.nt --validate
```

Für die Python-Umgebung gelten `requirements-validation.txt` und beim Comext-Adapter zusätzlich das aktuelle provider-datasets-Paket. Neue Ausgabeziele wählen; bestehende Projektionen werden nicht überschrieben. Nach fachlich geprüften Änderungen die Releasepins bewusst mit `python tools/update_current_manifest.py --write` erneuern und die Prüfungen wiederholen. Der Validator repinnt keine Dateien automatisch.

## Umsetzung als nächste Arbeit

1. GENESIS-Konverter gegen das geprüfte Statistikmodell umsetzen: Indizes, GP9-Mengen, Quartale, Einheiten/Stickstoffbasis, fehlende Werte und Quellenkennzeichen.
2. Bestehende Producer nacheinander mit expliziten Adaptern migrieren: zuerst Häfen/CPPI, anschließend Mining und Ereignisse; Soja/Raster und Routing mit ihren jeweiligen Zeit- und Identitätsregeln. Pro Migration alte/neue Beispielergebnisse vergleichen und Pins bewusst aktualisieren.
3. Modellpartner prüfen die Kompetenzfragen und offenen Definitionen; Produktions-/Veröffentlichungsumfang anschließend konkret festlegen. Keine stille Umschaltung bestehender Dagster-Läufe.

Das lokale Review ist umgesetzt. Produktionsmigration, formale Partnerabnahme und öffentliche Bereitstellung sind eigenständige noch offene Schritte.
