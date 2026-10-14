# Einzeln geprüfte logische Korrekturen

- `mining:rawRecordJson`: Dateneigenschaft bleibt erhalten. `rdf:JSON` als Range wurde durch `rdfs:Literal` ersetzt, damit der OWL-Parser daraus keine Objekteigenschaft erzeugt. Historische JSON-Literale bleiben zulässig; die JSON-Syntaxprüfung ist Aufgabe des Datenprofils.
- `mining:transportDestination` und `ports:relation`: Range `rdfs:Resource`/`rdf:Property` sind reservierte RDF-Metamodellbegriffe, keine OWL-DL-Klassen. Range nun `owl:Thing`; IRI- und Beziehungsprüfung bleiben in SHACL. Keine Identität wird daraus abgeleitet.
- Einstellige Property-Chain `isConnectedTo ← (connectsTo)` ersetzt durch semantisch entsprechende einfache Untereigenschaft `connectsTo ⊑ isConnectedTo`. Keine neue Transitivität oder Symmetrie.
- Genau die Beschreibungsgruppe des Beispielindividuums `https://provider.example.org/resource/dataset/cppi-2025` wird unverändert in `examples/current/cppi-edition-description.ttl` verschoben. Schema und Editionsexemplar sind getrennt; keine Quellenaussage gelöscht.
- Externe Referenzdeklarationen machen die bereits benutzten Klassen und Annotationseigenschaften explizit. Sie übernehmen keine fremden Axiome. Nur BFO wird im optionalen Alignment mit seinem offiziellen gepinnten Kern geprüft.

Die Eingangsverletzungen sind in `owl-dl-before.txt` erhalten. Die Nachprüfung und ihre tatsächliche Aussagekraft werden separat protokolliert.

- CPPI-Quellresultate waren weiterhin als SOSA-Aktivitäten deklariert. Beide Resultatklassen sind nun Unterklassen von core:Observation; forPort verweist auf observedFor. Dies setzt die bereits im Mining- und Kernmodell verwendete Trennung von Aktivität und Informationsergebnis konsequent fort.

- Drei undefinierte Event-Ranges durch vorhandene Begriffe ersetzt: InfrastructureAsset im Kern, Route im Kern; der heterogene Supply-Chain-Bezug bleibt owl:Thing statt eine unbegründete neue Node-Klasse einzuführen.
- Lokale Kompatibilitätsbegriffe Port/TradeLocation und Mining AlignmentRelation werden im jeweiligen eigenen Modul explizit deklariert und beschriftet.
- Die historische Quellbrücke SourceRecord → ports:SourceRecord entfällt: Ein allgemeiner GENESIS-Beleg darf nicht automatisch ein Hafenbeleg werden. Die korrekte umgekehrte Spezialisierung bleibt erhalten.
