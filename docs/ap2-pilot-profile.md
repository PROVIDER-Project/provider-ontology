# Gemeinsames AP2-Modellprofil — J1-07

Stand 04.10.2026, `provider-ap2-pilot` **0.1.0-rc1**, lokaler Reviewkandidat. Das Profil legt die Regeln für den begrenzten Santos–Hamburg-Pilot fest. Die Kernontologie bleibt Version 0.2.0. Partnerreview, reale Hafenidentitäten und Quellenfreigaben werden damit nicht als abgeschlossen erklärt.

Die maschinenlesbare [Profilreferenz](ap2-pilot-profile.json) bindet Dateien und Beispiele durch SHA-256. Die [Profilontologie](../ontology/ap2-pilot-profile.ttl) ergänzt die bestehenden Module; die separate [Quellenzuordnung](../ontology/ap2-source-alignment.ttl) ist ausdrücklich zuzuschalten. Alte Dataset-Manifeste behalten ihr bisheriges Profil `provider-source-vocabularies` 1.0.0 mit `reference-only`-Status. Ein Verweis auf diesen neuen Reviewkandidaten allein macht ihre Graphen nicht konform.

## Begriffe und Beziehungen

| Begriff | Bedeutung und bestehender Bezug | Pilotregel |
|---|---|---|
| `OperationalPort` | Operativer Hafen als Facility; Unterklasse von Core `Facility` und Infrastructure `Port` | Kanonische Identität unabhängig vom Quellcode |
| `Terminal` | Maritimes Terminal als Facility | Eigenes Objekt, `terminalOfPort`; das vorhandene Infrastructure `Terminal` bezeichnet ein **Flughafenterminal** |
| `PortArea` | Geografische Hafenfläche | Eigenes GeoSPARQL-Feature, `areaOfPort` |
| `TradeLocation` | Kodierter Handelsort, z. B. UN/LOCODE | Keine physische Hafenidentität allein aus Funktion 1 oder gleichem Namen |
| `SourceRecord` | Zeile/Feature mit Release-/Artefaktbezug | Rohwerte und Zeilenevidenz erhalten; keine Facility |
| `SourcePortFeature` | Quellenabhängiges Hafenobjekt | Bestätigte Zuordnung über `describesOperationalPort` |
| `Observation` | Informationsobjekt mit Beobachtungstag und Mess-/Schätzwerten | Spezialisierung der Core-Beobachtung; eigenes beobachtetes Objekt über `observedFeature` |
| `ObservationActivity` | Vorgang der Beobachtung/Schätzung | SOSA-Aktivität mit `sosa:hasResult`; von Ergebnis und Abruf getrennt |
| `Event` / `EventEpisode` | Ereignis versus quellspezifischer Episode/Version | Episode verknüpft über `episodeOf`; Episodewerte nicht ungeprüft auf das Gesamtereignis kopieren |
| `MatchAssertion` | Gerichtete, evidenzgebundene Zuordnung | Subject, Relation, Object, Status und Evidenz; bestätigte Beziehung zusätzlich mit Reviewperson/-zeit |

`Facility` wird aus dem Core wiederverwendet, nicht erneut parallel definiert. Im begrenzten Profil bekommen operativer Hafen, Handelsort, Quellrecord, Hafenfläche und Terminal getrennte Knoten und Rollen. Die entsprechende Disjunktheit gilt für diese profilierten Klassen; sie ist keine pauschale Aussage über sämtliche externen Vokabulare oder reale räumliche Überlappung.

Die Unterscheidung der Beobachtungen ist erforderlich: Das vorhandene BFO-Alignment klassifiziert Core `Observation` unter BFO `BFO_0000031` (Informationskategorie). Das Profil setzt sie deshalb nicht mit der SOSA-Beobachtungsaktivität gleich. Bestehende PortWatch-Quellressourcen behalten ihre bisherigen SOSA-Typen; ihre Quellenzuordnung führt zu `SourceObservation`, nicht automatisch zum kanonischen Informationsobjekt. Der spätere Adapter erzeugt ein separates Ergebnis und, wenn benötigt, eine separate Aktivität.

Ein bestätigter PortWatch-Bezug ist `SourcePortFeature → describesOperationalPort → OperationalPort`. Die Handelsortbeziehung hat die andere Richtung: `OperationalPort → servesTradeLocation → TradeLocation`. Fläche und Terminal bleiben eigene Objekte. Gleiches LOCODE, Namensähnlichkeit, Nähe oder ein hoher Matcher-Score liefern Evidenz für Kandidaten, aber keine Gleichsetzung.

## Identifikatoren, Namensräume und Versionen

| Verwendung | Festlegung |
|---|---|
| Autoritativer Core | `http://projekt-provider.de/ontology/`, 0.2.0, Commit `ea060ca…` |
| Pilot-Erweiterung | `http://projekt-provider.de/ontology/ap2-pilot#`, 0.1.0-rc1 |
| Quellenkompatibilität | Begrenzte explizite Klassenabbildung aus `https://projekt-provider.de/ontology/` und PortWatch; keine globale HTTP-/HTTPS-Gleichsetzung |
| Reale kanonische Hafen-IDs | Vorgeschlagene Basis `https://projekt-provider.de/id/port/<persistierte-UUID>`; Register und Aliasgeschichte entscheiden über Vergabe |
| Quellen-IDs | PortWatch-ID/URI und UN/LOCODE-URI bleiben erhalten; Aussagen und Records tragen Release-/Artefaktkontext |
| Reale Artefaktgraphen | Bestehende Basis `https://w3id.org/provider/graph/<dataset-id>/<artifact-id>` |
| Eigene Beispiele | `https://example.org/ap2/`; durchgängig synthetisch |
| PDL | Bestehender Partnernamensraum `https://provider-project.org/ontology/pdl#` |

Identische lexikalische Endungen unterschiedlicher Namespaces sind kein Identitätsnachweis. [Namespaceinventar](ap2-namespace-audit.json) und [gezielte Legacy-Migrationsentscheidungen](ap2-legacy-migration.json) dokumentieren die geprüften Grenzen. Keine globale Stringersetzung, kein neues `owl:sameAs` für HTTP/HTTPS und keine automatische Umschreibung vorhandener Graphen. Geänderte Quellenwerte erhalten einen neuen Artefaktgraphen; eine Quellen-ID ohne Graph-/Releasekontext allein bezeichnet keinen unveränderlichen Datenstand.

Das bestehende Hafenalignment mit `provider.example.org` und Demo-IDs wie `PWSSZ`/`PWHAM` bleibt didaktisches Vorbild. Seine automatischen bzw. als „manual“ markierten Beispielentscheidungen ersetzen kein artefaktgebundenes Review realer `port1160`-/`port446`-Records. Bei einer späteren Migration werden tatsächlich reale alte Register-IDs durch ein geprüftes Aliasregister erhalten; synthetische IDs werden nicht zu Produktions-IDs umgedeutet. UUIDs dürfen bei einem neuen LOCODE, Namens- oder Koordinatenstand nicht ohne Identitätsreview neu vergeben werden.

Die getrennte Quellenzuordnung enthält sechs Klassenbeziehungen: PortWatch/HTTPS-Port → SourcePortFeature, HTTPS-TradeLocation → TradeLocation, HTTPS-SourceRecord → SourceRecord und zwei tägliche PortWatch-Beobachtungstypen → SourceObservation. Quellenprädikate und fremde Klassen bleiben erhalten. AIS-/statistische Beobachtungsgebiete aus dem früheren Hafenregister werden nicht automatisch zu physischen Hafenflächen. Statische Schätzprofile, Chokepoint-Geometrien, GDACS und HS erhalten keine erfundene globale Klassenäquivalenz.

## Länder, Zeiten, Einheiten und fachliche Grenzen

- ISO2 und ISO3 bleiben getrennte Felder. BR/BRA und DE/DEU werden für den Pilot explizit geprüft. Ein Landeswiderspruch zwischen Quellhafen, kanonischem Hafen und Handelsort blockiert die bestätigte Zuordnung. Eine allgemeine Umsetzung braucht die versionierte Länderreferenz; Namen oder die ersten zwei Zeichen eines ISO3-Codes reichen nicht.
- Tagesbeobachtungen verwenden `xsd:date`. Die vorhandene PortWatch-SOSA-Zeit um 00:00 UTC kann die Tageskodierung sein; sie ist kein nachgewiesener Mess- oder Abrufzeitpunkt. Abrufzeit bleibt im separaten Manifest-Laufbeleg. UN/LOCODE-`Date` bleibt der rohe Quelltoken, z. B. YYMM, statt als Tagesbeobachtung interpretiert zu werden.
- Hafenanläufe sind ganzzahlige Anlaufzahlen, keine Anzahl eindeutiger Schiffe. Tägliche Import-/Exportwerte sind nichtnegative Dezimalwerte mit Einheit metrische Tonne und AIS-Schätzcharakter. Der [IMF-Methodenbericht](https://www.imf.org/-/media/files/publications/wp/2025/english/wpiea2025093-print-pdf.pdf) beschreibt diese Shipment-Schätzung. Einheitenbezeichnungen begründen keine Genauigkeits- oder Commodity-Behauptung.
- Durchschnittliche statische Flottenprofile können Dezimalwerte tragen; sie werden nicht mit täglichen ganzzahligen Anläufen gleichgesetzt. Chokepoint-`capacity`, Trade-Shares, Rankings und Verbindungsgewichte bleiben quellspezifisch. Eine Kapazitätsschätzung ist keine zugesicherte technische Terminalkapazität.
- PortWatch-Gesamttonnage und „Vegetable Products“ sind keine beobachteten Sojamengen. HS-Kategorien und das getrennte `soy-backtest-filtered`-Produkt liefern anderen Kontext; ein Sojaanteil müsste als zusätzliche Annahme/Evidenz modelliert werden.
- GeoSPARQL-Punkte und Flächen bleiben unterschiedliche Repräsentationen. Standard-WKT-Punkte benutzen Längengrad vor Breitengrad. Nähe beweist keine Identität. Ein GDACS-Ereignis und räumliche Nähe beweisen keinen tatsächlich eingetretenen Hafenausfall oder Lieferketteneffekt.

## PROVIDER–PDL-Alignment

Verifiziertes öffentliches Partnerartefakt: [PDL `spec/pdl-ontology.ttl` im Commit `7b442bac…`](https://github.com/PROVIDER-Project/provider-pdl/blob/7b442bac5a00d5ede62dd0736efd5a790a7a259a/spec/pdl-ontology.ttl), Version **1.2**. Die betrachteten lokalen Viewer-/PEARL-Kopien stehen noch auf 1.1 und ersetzen diese Referenz nicht. Die unveränderte Testkopie und ihre Prüfsumme sind dokumentiert; Imports werden bei Offline-Prüfungen nicht automatisch aus dem Netz geladen.

`pdl:Infrastructure` wird über `representsFacility` mit einer konkreten PROVIDER-Facility verbunden. `pdl:Event` kann über `representsEvent` ein konkretes Ereignis referenzieren. Das sind vorgeschlagene explizite Repräsentationsrelationen für den Pilot; keine Klasse wird global mit Core `Facility`, `OperationalPort` oder `Event` gleichgesetzt. Ein angenommenes PDL-Ereignis bleibt ein Szenarioanteil und wird nicht allein durch den Bezug zu einer beobachteten Tatsache. Beim Szenarioexport sind Annahmen und beobachtete Daten getrennt auszuweisen.

## Beispiele, Prüfungen und Review

Die vier RDF-Dateien unter `examples/ap2-pilot/` enthalten **eigene erfundene** PortWatch-/UN/LOCODE-Eingänge und einen kleinen kanonischen Graphen. Namen und Codes Santos/Hamburg dienen nur zur Veranschaulichung; Werte, Geometrien, Terminal, Fläche, Ereignis und „accepted“-Zuordnungen sind synthetisch. Die drei Quellen-N-Triples-Dateien wurden mit dem vorhandenen Paket 0.6.0 erzeugt und geprüft; Eingänge und reproduzierbarer Builder liegen in `provider-datasets/examples/ap2-pilot/`. Kein Realreview wurde erzeugt.

Offline-Prüfung mit Python und `rdflib==7.6.0`:

```bash
python tools/check_ap2_profile.py
python -m unittest discover -s tests -p 'test_*.py'
```

Die 20 Tests sichern die gepinnten Referenzen, getrennte Rollen, Zuordnungsrichtungen, Evidenz/Review, Länder, Beobachtungstage, Einheiten und die PDL-/Episodenbezüge ab. Sie sind gezielte ausführbare Pilotregeln, **keine vollständige OWL-Konsistenzprüfung oder SHACL-Baseline**. J1-09 erstellt daraus versionierte Shapes und eine umfassendere Abnahme.

Die echten lokalen Kandidaten sind `port1160`/Santos → BRSSZ und `port446`/Hamburg → DEHAM. Beide UN/LOCODE-Einträge haben auch maritime Funktion, zugleich weitere Funktionen. Damit passen sie zum Relationstyp `servesTradeLocation`; eine tatsächliche physische Hafenidentität ist damit noch nicht bestätigt. Eingangschecksummen, Quellzeilen und Länder-/Konfliktbeispiele bleiben im lokalen AP2-Arbeitsbereich, nicht in den Repositories. Die vorhandene Reviewliste enthält 977 offene Fälle; keine Entscheidung wird hier vorweggenommen.

[Partnerreview-Matrix](ap2-pilot-review.md). J1-07 ist lokal als überprüfbarer Modellvorschlag umgesetzt. Die Partnerbestätigung der fachlichen Entscheidungen bleibt offen. J1-08 kann den begrenzten Demonstrator anhand dieses Profils entwickeln, hält reale Zuordnungen aber bis zum Review als Kandidaten zurück.
