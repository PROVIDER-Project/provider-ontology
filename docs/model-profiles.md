# Fachprofile im Kandidaten 0.3.0-rc3

Namespace: `https://projekt-provider.de/ontology/`. Der vollständige Einstieg `ontology/current/provider.ttl` bleibt für Gesamtprüfungen verfügbar. Anwendungen wählen unter `ontology/current/profiles/`:

| Profil | Verwendung |
|---|---|
| core | Allgemeine Anlagen, Akteure, Ergebnisse, Messwerte, Quellen und qualifizierte Aussagen |
| transport | Straßen-/Bahnobjekte, getrennte Topologie, gerichtete Traversierungen und Sperrszenarien |
| statistics | GENESIS, Comext, Klassifikationen, Perioden, fehlende Werte und Einheiten |
| maritime | Häfen, CPPI, Routentopologie und gemeinsame Messwerte |
| mining | Anlagen, Materialien, Quellenintegration und gemeinsame Messwerte; ohne Pilot/Matching-Erweiterungen |
| events | Ereignisse und Gefährdungen; zusätzliche Supply-Chain-Strukturen werden nicht vorausgesetzt |
| supply-chain | Stufen, Rollen, Flüsse und Risikostrukturen |
| bfo | Optionales BFO-Alignment und dessen lokaler Kernimport |
| all | Gesamtes Modell einschließlich optionaler Erweiterungen, nur für integrierte Prüfung |

`review_current.load(profile="statistics")` lädt ausschließlich die rekursive lokale Importabschlussmenge dieses Profils. Unbekannte Profile, veränderte Hashes und ungelöste Modulimporte werden abgewiesen. Der XML-Katalog unterstützt lokale Ontologieeditoren. Die eigenen Module bleiben getrennt; Quellenvokabulare werden nur im benötigten Fachabschluss geladen.

## Gemeinsames Ergebnismuster

Informationsergebnis → `hasMeasurement` → Messwert mit `measurementValue`, `measurementKind`, `hasUnit`. Dazu `observedFor`, Referenzperiode und `sourceRecord`. Hafen- und CPPI-Eigenschaften sind Untereigenschaften dieser allgemeinen Beziehungen. Mining-Direktwerte werden durch einen expliziten Adapter auf Messwertknoten projiziert; keine Umdeutung der historischen Literal-Einheit in eine Objekt-Eigenschaft.

Eine dokumentierte Quelle benötigt einen SHA256 und entweder einen tatsächlich bekannten `acquiredAt`-Zeitpunkt mit Zeitzone oder `sourceCheckedOn` mit Tagesgenauigkeit. Ein Prüfdatum ist kein erfundener Abrufzeitpunkt. Produktionsumfang (`total`/`sold`), Mengenbasis (`t-N`), Indexbasis, Originalwert und Qualitätsmarker bleiben getrennt. Unterdrückte Werte und nicht verfügbare Werte erhalten keine Messwertknoten.

Die Module ändern weder die Bestandskonverter noch historische produktive Pins automatisch. Die rc1-Modelldateien sind unter `docs/review/2026-10-14/rc1/` gesichert; ältere Prüfberichte gelten für diesen eingefrorenen Kandidaten.
