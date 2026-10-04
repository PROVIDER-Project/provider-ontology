# J1-09: Lokale Modell- und SHACL-Baseline

Stand: 2026-10-04. Version 0.1.0-rc1, lokaler Review-Kandidat. Die technische Umsetzung ist lokal prüfbar; Partnerreview und fachliche Quellen-/Hafenfreigaben bleiben offen.

## Verbindliche Module

`ap2-shacl-baseline.json` enthält Dateiprüfsummen, Ontologie-IRIs, Versionen und deklarierte Imports für Core 0.2.0, Infrastruktur 1.0.0, AP2-Profil und Quellenalignment 0.1.0-rc1, BFO-Alignment 0.2.0 sowie die unveränderte PDL-Referenz 1.2. Alternative XML-Serialisierungen, zusätzliche Netzwerk-/Supply-Chain-Module und lokale Entwürfe gehören nicht zu dieser Baseline. Die J1-07-Dateien bleiben unverändert.

Der öffentliche develop-Stand enthält identische Core-, Infrastruktur- und BFO-Dateien. Die beiden neuen AP2-Module sind dort noch nicht vorhanden. Der gespeicherte Vergleich nennt Remote-Commit und Abrufzeit; diese Baseline ersetzt keine öffentliche Veröffentlichung.

## Ausführen

```sh
python -m pip install -r requirements-validation.txt
python tools/validate_ap2_shacl.py --data-kind synthetic --output /tmp/ap2-shacl
python -m unittest discover -s tests -p 'test_*.py'
```

Eigene kohärente Datensichten mit wiederholtem `--data DATEI.ttl` beziehungsweise `.nt` prüfen. `--profile source --data-kind real` prüft Quellen und offene Review-Kandidaten. `--profile canonical` prüft zusätzlich kanonische Häfen, Beobachtungsergebnisse, Messwerte, Aktivitäten und PDL-Repräsentationen. Kanonische Entitäten werden im Quellenprofil abgelehnt. Reale und synthetische Sichten getrennt prüfen. Rückgabewert 0 bedeutet konform, 1 Regelverletzung oder Ausführungsfehler; nur vorhandene Berichte mit `conforms: true` bestätigen Erfolg.

Ausgaben: standardkonformer RDF-SHACL-Bericht `report.ttl` und maschinenlesbare `summary.json`, einschließlich Baseline-Prüfsumme und Laufzeitversionen. Dateipins werden vor jeder Prüfung kontrolliert. Kein Netzabruf, keine automatischen OWL-Imports und keine Domain/Range-Inferenz: ausschlaggebend sind die expliziten Klassenhierarchien der gepinnten Module.

## Prüfumfang

Geprüft werden HTTP-IRIs, Pflichttypen, ISO-Codes, CRS84-Punktgrenzen, Datum/Reviewzeit, nichtnegative Messwerte, Tonnen gegenüber Anzahlen, ganzzahlige Hafenanläufe, Quellenwerte und Beobachtungsbezug, Ergebnis/Aktivität, Event/Episode, Provenienz sowie evidenzgebundene Reviewentscheidungen. Offene oder abgelehnte Matches dürfen keine bestätigten Beziehungen erzeugen. Jede materialisierte Hafenbeziehung braucht einen akzeptierten, dokumentierten Match mit passenden Rollen und Ländern. Globale sameAs-/Äquivalenzbehauptungen sind im Pilot verboten. Leere oder fachfremde Graphen bestehen die Prüfung nicht.

Die vorhandene gültige Vier-Dateien-Fixture wird mit 20 gezielten Fehlerfällen ergänzt (`examples/ap2-shacl/negative-cases.json`). Dazu kommen Punktgrenzen, leere Graphen, Profilauswahl und unveränderte Eingaben. Die Gegenbeispiele sind ausschließlich selbst erzeugte Datenänderungen.

Grenzen: Länderpaarprüfung derzeit BR/BRA und DE/DEU; keine vollständige OWL-Konsistenzprüfung, keine globale OSM-/GDACS-/Soja-Abdeckung, keine Polygon-Topologie oder CRS-Transformation. SHACL-Konformität erteilt keine Identitäts-, Rechte- oder Partnerfreigabe.

Grundlagen: [W3C SHACL](https://www.w3.org/TR/shacl/), [PySHACL](https://github.com/RDFLib/pySHACL). Öffentliche Freigabe erst nach Partnerreview und separater Quellenprüfung.
