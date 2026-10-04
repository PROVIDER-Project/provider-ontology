# Reviewmatrix für das AP2-Pilotprofil 0.1.0-rc1

Keine Partnerfreigabe wird durch diese Datei erteilt. Die nachstehenden Entscheidungen sind lokal implementierte Vorschläge mit ausführbaren Beispielen und noch offenem Partnerreview. Reale Quellenrechte und konkrete Matchfreigaben werden separat artefaktgebunden geführt.

| Entscheidung | Vorschlag / Evidenz | Status / zuständiger Review |
|---|---|---|
| Hafen, Terminal, Fläche, Handelsort | Getrennte profilierte Klassen; vorhandenes Infrastructure Terminal ist ein Flughafenbegriff | Lokal geprüft; InfAI/Modellpartner offen |
| Beobachtungsergebnis vs. Aktivität | Core/BFO-Information getrennt von SOSA-Aktivität; SourceObservation separat | Lokal geprüft; Modellpartner offen |
| Namespace und Identifikatoren | HTTP-Core beibehalten, Quellen-HTTPS explizit abbilden; neue Hafen-IDs aus persistentem Register | Lokal geprüft; Projekt-Namespace-/Registerentscheidung offen |
| PDL-Alignment | Version 1.2 gepinnt; representsFacility/representsEvent statt globaler Äquivalenz | Lokal geprüft; PDL-Partner offen |
| Einheiten und zeitlicher Bezug | Tage/Abrufzeiten trennen; Anläufe und metrische Shipment-Schätztonnen mit Quellencharakter | Lokal geprüft; fachlicher Review offen |
| Santos/Hamburg | port1160–BRSSZ, port446–DEHAM als Kandidaten für servesTradeLocation | Realreview pending; keine bestätigten Produktionsedges |
| Länderwidersprüche | Bestehende Reviewfälle port1117 und port1426 blockieren automatische Zuordnung | Fachliche Klärung offen |
| Räumliche Abweichung / Revisionsstand | Bestehender hoher Reviewfall port1364; Nähe allein unzureichend | Fachliche Klärung offen |
| Veröffentlichung / Shapes | Lokaler RC, keine Tag-/Quellenfreigabe; vollständige SHACL-Abnahme folgt J1-09 | Offen |

Reviewentscheidungen müssen die konkrete Profilversion sowie die betroffenen Artefakt- und Recordversionen nennen. Ein accepted-Testbeispiel mit `dataKind Synthetic` ist kein Beleg für einen realen Match. Die offene Reviewliste wird nicht automatisch verändert. Die bestehenden QLever-Freigaben verlangen weiterhin die konkrete Artefakt-ID und Manifestchecksumme.
