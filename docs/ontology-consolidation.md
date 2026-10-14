# PROVIDER: Konsolidierung des Modells und Echtdatenabnahme

Stand: 14.10.2026, lokaler Kandidat **0.3.0-rc2**, Namespace `https://projekt-provider.de/ontology/`.

## Beurteilung des Modellumfangs

Das Modell kann die derzeitigen AP2-Daten ausdrücken. Es ist als Gesamtmodell deutlich umfangreicher als der nachgewiesene aktuelle Bedarf. Die Bestandsaufnahme des rc1 umfasst 905 eigene Klassen/Eigenschaften: 105 werden durch Beispiele oder Kompetenzfragen ausgeübt, sechs weitere sind nur im Quellenregister direkt zugeordnet, zwölf sind veraltete Kompatibilitätsbegriffe. 782 sind bislang nicht ausgeübte Erweiterungen. Diese Kategorien sind kein Beweis für Redundanz oder Löschbarkeit. SPARQL-Präfixe werden bei der Zuordnung aufgelöst; deshalb korrigiert die reproduzierbare Zählung die erste konservative Übersicht von 98 auf 105 ausgeübte Begriffe.

**Entscheidung:** Den Pflichtumfang durch Fachprofile begrenzen. Klassen und Eigenschaften werden aufgrund ihrer fachlichen Bedeutung und benötigten Abfragen ausgewählt; kein weiteres Modell pro Jahr, Tabellenkennung oder Produktcode. Große Event-/Supply-Chain-Erweiterungen, Mining-Matching und BFO bleiben gesondert wählbar. Bestehende Begriffe werden nicht blind gelöscht. Alle Entscheidungen und Verwendungen stehen in `review/2026-10-14/granularity-*.json`.

## Gemeinsames Muster

Ein Informationsergebnis verweist auf Messwert, Mengenart, kontrollierte Einheit, Referenzperiode und Quelle. Hafen- und CPPI-Eigenschaften schließen an die Kernbeziehungen an. GENESIS und der Mining-Kapazitätspilot erzeugen explizite Messwertknoten. Quellengraphen bleiben unverändert; die Adapter produzieren separate Projektionen.

Menge, Kapazität, Index und Rang bleiben fachlich verschieden. `t-N` zählt enthaltenen Stickstoff; nicht die Masse des Endprodukts. `total` und `sold` werden nicht summiert. Indexbasis und statistische Bereinigung bleiben sichtbar. Fehlwerte erhalten keine künstliche Null. Das GENESIS-Zeichen `-` kann statistisch geheimhaltungsbedingt sein und wird deshalb nicht als sichere gemessene Null ausgegeben.

Quellenhashes und Rechte werden erhalten. Ein dokumentierter Prüftag darf über `sourceCheckedOn` angegeben werden; ohne Beleg wird kein exakter Abrufzeitpunkt erfunden. CPPI-Quellresultate sind Informationsergebnisse, keine SOSA-Aktivitäten. Allgemeine Quellenbelege werden nicht automatisch zu Hafenbelegen.

## Abnahmeumfang

- 42 Regressionstests und 31 bestehende Kompetenzfragen; positive und negative Datenfälle.
- OWL-2-DL-Profilprüfung mit ROBOT 1.9.11 und HermiT-Konsistenz/Klassenkohärenz über alle eigenen Module plus offiziellen, lokal gepinnten BFO2020-Kern. Positive Domain/Range-Proben sowie erwartete Zurückweisung einer widersprüchlichen Fehlwertinstanz und einer unmöglichen BFO-Klasse.
- GENESIS: alle 1.680 versionierten Zellen der drei vorhandenen Ausschnitte. 1.102 numerische Ergebnisse, 578 unbestimmte Zellen. Tabellen61241-0006,42153-0003,42131-0002; GP9 umfasst 720 Zellen. Alle Werte/Originalzeichen/Qualitätsmarker und Produktionsumfänge bleiben erhalten.
- CPPI: alle 2.212 tatsächlich berichteten kombinierten Scores aus dem lokalen, offiziell authentifizierten Annex; darunter 806 negative Werte. Nur Score-Projektion, keine neue Hafenidentitätsentscheidung. Ränge, Komponenten und operative Kennzahlen bleiben außerhalb dieser begrenzten Projektion in der Quelle.
- GEM: erste 20 Quellzeilen des gepinnten lokalen Mai2026-Workbooks, Blatt Non-closed mines; zehn vorhandene Kapazitätswerte. Tonnen/Jahr nach vorhandener Konverterskalierung. Keine behauptete tatsächliche Produktion, Betreiberfreigabe oder ICMM-Verknüpfung.
- Comext: bestehende vollständige Projektion mit 3.960 Zellen als Regression gegen rc2; Ergebnis in den datierten Nachweisen.

Die gemeinsame Abfrage `queries/common-measurements.rq` arbeitet auf allen vier Projektionen und gruppiert nach Mengenart und Einheit. Sie summiert keine unvereinbaren Größen und ersetzt weder die Quellenprüfung noch die fachliche Interpretation.

## Reproduzieren

Python-Umgebung: `requirements-validation.txt`. Für die Echtdatenadapter zusätzlich die aktuelle Installation von `provider-datasets` und dessen Mining-Abhängigkeiten; alternativ dessen `src/` über PYTHONPATH. Java11+ für ROBOT.

```sh
python -m unittest discover -s tests -v
python tools/review_current.py --data examples/current/ap2-example.ttl --output output/review.json
python tools/audit_granularity.py --output output/granularity.json
python tools/fetch_reasoner.py --output output/tools/robot.jar
python tools/check_current_logic.py --robot-jar output/tools/robot.jar --output output/logic
python tools/project_genesis.py --datasets-root ../provider-datasets --output output/genesis/provider.nt
PYTHONPATH=../provider-datasets/src python tools/project_comext.py --bundle ../provider-datasets/output/comext/2026-10-13 --output output/comext/provider.nt --validate
PYTHONPATH=../provider-datasets/src python tools/project_domain_pilots.py --cppi /ABSOLUTER/PFAD/CPPI_2020_2025.xlsx --gem /ABSOLUTER/PFAD/GEM.xlsx --gem-sheet 'Non-closed mines' --gem-limit 20 --output output/domains
```

Der ROBOT-Download wird gegen den festgelegten SHA256 geprüft. Modellimporte sind offline und dateigepinnt. BFO behält CC BY4.0 und seine eigenen Metadaten; ROBOT ist BSD-3-Clause. Andere referenzierte externe Vokabulare werden lediglich deklariert; die Prüfung behauptet keine vollständige externe PROV/SOSA/GeoSPARQL-Axiomabschlussmenge. Kalenderlexik und Datenvollständigkeit prüft SHACL.

## Nutzungs- und Integrationsgrenzen

GENESIS-Belege: Datenlizenz Deutschland Namensnennung2.0 gemäß vorhandenen Erfassungsmanifesten. CPPI-Annex: CC BY-NC3.0 IGO, keine pauschale kommerzielle Freigabe. Beim lokalen GEM-Workbook ist die genaue Wiederverwendung weiterhin offen; der Pilot setzt keine Lizenzbehauptung und darf nicht als Datenfreigabe präsentiert werden. Alle vollständigen Roh-/Projektionsgraphen bleiben im ignorierten lokalen Output. Das Partnerpaket enthält Modell, Werkzeuge und Prüfberichte, keine echten Annex-/Mining-Rohdaten.

Es erfolgte keine automatische Umstellung der Bestandskonverter, Workflow-Pins oder des produktiven Knowledge Graph. Nächster Umsetzungsblock: Kandidat rc2 fachlich mit den Partnern abstimmen und anschließend die geprüften Projektionen als reguläre, versionierte Konverterverträge in provider-datasets übernehmen. Danach Workflow-Pins gezielt migrieren; akzeptierte Identitäten und qualifizierte Verknüpfungen getrennt prüfen. Granularität insbesondere für Ereignisbewertungen, Lieferkettenrollen und Anlagenkapazität weiter an realen Kompetenzfragen absichern.

## Nachweise und technische Referenzen

Datierte JSON-Berichte unter `docs/review/2026-10-14/`; PDF und reproduzierbares Modellpaket unter `reports/ontology-review/2026-10-14/`. Frühere rc1-Berichte bleiben historische Belege.

[ROBOT reason](https://robot.obolibrary.org/reason) · [OWL-Profilprüfung](https://robot.obolibrary.org/validate-profile) · [offizieller BFO2020-Kern](https://github.com/BFO-ontology/BFO-2020) · [SHACL](https://www.w3.org/TR/shacl/)
