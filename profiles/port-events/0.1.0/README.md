# Grobes Hafenereignisprofil 0.1.0

Dieses optionale Anwendungsprofil liegt auf dem unveränderten Ontologiekandidaten 0.3.0-rc3. Es ergänzt weder neue Ereignisklassen noch globale Inferenzregeln. Manifest, Basisdateien, eigenes Profil und SHACL sind gehasht. Die aktuelle Release-Datei wird nicht umgeschrieben; bisherige Transport-/Statistik-/Demonstrator-Pins bleiben unverändert.

## Projektniveau

Ein Ereignis besitzt Quellenbezug und einen belegten Zeitraum, gegebenenfalls nur als Text. Eine `EvidenceAssertion` qualifiziert die Aussage über ein ausdrücklich genanntes Ziel. Granularität: Hafen, Terminal, Korridor, Region, Organisation oder ein ausdrücklich genanntes Teilobjekt. Keine Straßensegmente, Torknoten oder Routengraphen erforderlich. OSM-Analyse ist eine separate optionale Evidenzquelle.

Wiederverwendet werden `provider:Event`, `EvidenceAssertion`, `SourceRecord`, `assertionMode`, Zeit-/Quellenangaben sowie RDF-Reifikation und PROV. Die wenigen zusätzlichen Ausprägungen sind SKOS-Konzepte im Profilnamespace, keine neuen Klassen:

- Evidenzniveau: Kontext, räumliche Exposition, betriebliche Einschränkung, mögliche Wirkung.
- Funktion: Umschlag, Lagerung, Wasser-/Straßen-/Schienenzugang; zusätzlich allgemeiner Hafenbetrieb und nicht belegte Funktionsangabe.
- Ausmaß: vollständiges ausdrücklich genanntes Ziel, teilweise Einschränkung, nicht belegter Umfang.
- Zeitqualität: belegtes Fenster, nur Text, widersprüchliches Ende.

`OperationalRestriction` bedeutet eine laut Quelle berichtete (`Reported`) oder angekündigte (`Planned`) Einschränkung. Es ist keine automatische Aussage über tatsächlichen Vollzug oder heutigen Betrieb. `FullTarget` auf einer Durchfahrt bedeutet nur diese Durchfahrt, nicht den übergeordneten Hafen. Räumliche Exposition und mögliche Wirkung sind `Modelled` und benötigen eine ausdrückliche Methode/Annahme. Keine erfundenen Konfidenzzahlen.

## Quellenbindung und Zeit

Die reifizierte Aussage enthält Subjekt, Prädikat `provider:affects`, Zielobjekt, Evidenzniveau, Funktion, Ausmaß, Modus und Quelle. Eine gehashte Review-Basis bewahrt die manuell belegte Interpretation. SHACL verhindert eine nachträgliche Aufwertung gegenüber dieser Basis. Das ist eine Konsistenzprüfung und kein automatisches Sprachverständnis oder Beweis der Wahrheit einer Herausgeberangabe.

Direkte `affects`-/`causes`-Kurzschlüsse werden in diesem Profil abgelehnt. Übergeordnete Hafenbezüge dienen als Kontext und übertragen keine Einschränkung. Ereigniszeit, Veröffentlichungsdatum und Abrufzeit bleiben getrennt. Datums-/Zeitzonennormalisierung wird erklärt; aus „Sommer“ oder „nachts“ werden keine Uhrzeiten erfunden. Bei widersprüchlichem Ende bleibt `endTime` leer. Historische Meldungen werden nicht durch einen späteren Abruf zur aktuellen Betriebslage.

Die realen Fälle verwenden vorerst quellenlokale Zielreferenzen. Eine geprüfte Zuordnung zum kanonischen Hafenregister ist Schritt 3, kein impliziter Teil dieses Profils. Das Anwendungsprofil ist deshalb auch kein Ersatz für vorhandene Source-/PortWatch-/GDACS-Modelle.

## Ausführen

```sh
python tools/validate_port_events.py --data profiles/port-events/0.1.0/examples.ttl --output output/port-event-profile-example
python -m pytest tests/test_port_events.py
```

`examples.ttl` enthält ausschließlich erfundene Modelltests, darunter Exposition und mögliche Wirkung. Die vier realen Primärquellenfälle, das geprüfte RDF und die lesbare Auswertung liegen im benachbarten provider-datasets unter `catalog/ap21/port-events/2026-10-16/` bzw. `reports/port-events/2026-10-16/`.

## Umfang dieser Umsetzung

Schritt 1 (Anwendungsprofil) und Schritt 2 (kleine reale Fallsammlung) sind umgesetzt. Kanonisches Matching, automatische Funktions-/Wirkungszuordnung und Dagster-Job folgen separat. Keine öffentliche Quellen-/KG-Freigabe und keine Partnerabnahme werden daraus abgeleitet.
