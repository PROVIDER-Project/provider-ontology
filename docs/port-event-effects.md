# Bedingte Funktionsfolgen im Hafenereignisprofil

Stand 16.10.2026. Das unveränderte optionale Profil `profiles/port-events/0.1.0/` genügt für erste bedingte Funktionsfolgen. Die Implementierung und konkreten Quellenreviews liegen im Datasets-Repository unter `catalog/ap21/port-events/2026-10-16/impacts/`; das portable Artefakt unter `reports/port-events/impacts-2026-10-16/`. Kein neuer OWL-Release oder Eingriff in den gepinnten Modellkandidaten ist erforderlich.

## Aussageebenen

1. Die ursprüngliche qualifizierte Aussage bleibt `OperationalRestriction` und `Reported` oder `Planned`. Ziel, Quellzeitraum, Funktion und Umfang werden unverändert übernommen.
2. Eine zusätzliche `EvidenceAssertion` hat `PossibleImpact`, `Modelled`, `UnspecifiedExtent` und dieselbe Zielreferenz sowie eine durch die Quelle belegte Zugangsart. Ihre Aussage ist ausdrücklich bedingt; sie ist keine gemessene Folge oder bestätigte Kausalität.
3. `prov:wasDerivedFrom` verweist auf eine eigene Review-Basis mit Hash, Methode und Bearbeiter; diese Basis verweist auf die ursprüngliche Quellaussage. Die Review-Basis hält die gewählte Qualifikation fest, ist selbst aber kein unabhängiger Wirkungsbeleg.
4. `dct:requires` verweist auf eine explizite Annahme als `prov:Entity`. Deren `dct:valid` lautet `unverified-condition`; ihr Text beschreibt eine bisher nicht belegte Fahrt-/Zugangsabhängigkeit. `p:assumptionNote` erklärt Methode und Bedingung. Keine neuen Ontologiebegriffe nötig.

Für diese Methode werden ausschließlich Wasser-/Straßenzugangsfolgen betrachtet. Teilobjektbezüge werden nicht auf den ganzen Hafen übertragen. Eine Quellenreferenz darf über das Register einem Hafen zugeordnet sein; das ersetzt nicht das ausdrückliche Ziel der ursprünglichen Ereignisaussage. Der bedingten Folge wird kein erfundenes eigenes Zeitfenster hinzugefügt. Der Quellenzeitraum bleibt am Ereignis; ein widersprüchliches Ende bleibt offen.

## Prüfbarkeit und Grenzen

Das Datasets-Paket ergänzt das Profil um methodenspezifische SHACL-Regeln: ursprüngliche Einschränkung auf demselben Ereignis, Ziel und Funktion; Quellenmodus Reported/Planned; Ableitungsmodus Modelled; ausdrückliche unbestätigte Bedingung; keine direkte `p:affects`-/`p:causes`-Behauptung. Die Regeln prüfen formale Konsistenz, nicht die Wahrheit einer Bedingung oder eine kausale Wirkung.

Für eine tatsächliche Wirkungsaussage fehlen identifizierte Transporte, Abhängigkeits-/Nutzungsnachweise, zeitlicher Vollzug, Alternativen und beobachtete Istzeiten. Das Review dokumentiert diese Anforderungen pro Ziel. Für den Duisburger Gruppenbilanzkontext wird keine Hafenwirkung erzeugt. Weitere Funktionen wie Lagerung, Umschlag oder Schienenanbindung werden nicht aus allgemeinem Hafenwissen ergänzt.

Das Paket ist ohne Ontologie-Checkout mit RDF, lokalem Schema, den zusammengeführten SHACL-Regeln und gespeicherten Abfragen prüfbar. Die Partnerabnahme und Quellen-/KG-Veröffentlichungsfreigabe bleiben eigenständig.
