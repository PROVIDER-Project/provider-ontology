# Kompetenzfragen für PROVIDER

Stand 13.10.2026. Ausführbare Modelltests gegen ausdrücklich erfundene Daten; keine empirische Vollständigkeit oder Partnerabnahme.

| ID | Frage | Erwartung |
|---|---|---|
| [CQ01](../queries/competency/CQ01.rq) | Sind Organisation und betriebene Anlage getrennt? | True |
| [CQ02](../queries/competency/CQ02.rq) | Bleibt die physische Ware vom Klassifikationskonzept getrennt? | True |
| [CQ03](../queries/competency/CQ03.rq) | Bleiben leere Zellen ohne Zahlenwert und Ergebnisbehauptung? | True |
| [CQ04](../queries/competency/CQ04.rq) | Bleibt eine belegte Null als Zahlenwert erhalten? | True |
| [CQ05](../queries/competency/CQ05.rq) | Bleiben unvollständige Jahreswerte Teilsummen? | True |
| [CQ06](../queries/competency/CQ06.rq) | Sind Preisindex, Produktionsindex und Kapazität verschieden? | True |
| [CQ07](../queries/competency/CQ07.rq) | Ist t-N von Tonnen Warenmasse unterscheidbar? | True |
| [CQ08](../queries/competency/CQ08.rq) | Bleiben Statistikmonat, Provider-Update und Abruf getrennt? | True |
| [CQ09](../queries/competency/CQ09.rq) | Tragen gleiche Warencodes über 2022 unterschiedliche Jahresbezüge? | [['2021', 'HS2017'], ['2022', 'HS2022']] |
| [CQ10](../queries/competency/CQ10.rq) | Bleiben Hafenquelle, Hafenanlage und UN/LOCODE-Ort verschieden? | True |
| [CQ11](../queries/competency/CQ11.rq) | Ist eine GDACS-Episode getrennt vom Ereignis darstellbar? | True |
| [CQ12](../queries/competency/CQ12.rq) | Wird Teil-von bei Mining nicht als Identität ausgegeben? | True |
| [CQ13](../queries/competency/CQ13.rq) | Bleiben negative CPPI-Scores mit Jahresbezug gültig? | True |
| [CQ14](../queries/competency/CQ14.rq) | Bleiben Sojasaison und Maskenjahr getrennt? | True |
| [CQ15](../queries/competency/CQ15.rq) | Belegt eine OSM-Hafenfläche keine Anlagenkapazität? | True |
| [CQ16](../queries/competency/CQ16.rq) | Wird aus einer berechneten Seeroute keine beobachtete Fahrt? | True |
| [CQ17](../queries/competency/CQ17.rq) | Sind GENESIS-Quartale ohne künstliche Monatswerte darstellbar? | True |
| [CQ18](../queries/competency/CQ18.rq) | Sind Nutzungsbedingungen und Credit an der Datenquelle auffindbar? | True |
| [CQ19](../queries/competency/CQ19.rq) | Bleibt eine Szenarioannahme eine qualifizierte Aussage? | True |
| [CQ20](../queries/competency/CQ20.rq) | Sind gemeldete Fakten mit Quellenbelegen verknüpft? | True |
| [CQ21](../queries/competency/CQ21.rq) | Bleibt eine geplante Änderung vom beobachteten Betrieb getrennt? | True |
| [CQ22](../queries/competency/CQ22.rq) | Kann derselbe Abschnitt in zwei Routen verschiedene Positionen haben? | [['0'], ['3']] |
| [CQ23](../queries/competency/CQ23.rq) | Wird aus einer Gefahrenklasse kein realisierter Lieferausfall gefolgert? | False |
| [CQ24](../queries/competency/CQ24.rq) | Bleibt das Quellenkennzeichen einer fehlenden Zelle erhalten? | True |
| [CQ25](../queries/competency/CQ25.rq) | Bleiben Mining-Ergebnis und Beobachtungsaktivität getrennt? | True |
| [CQ26](../queries/competency/CQ26.rq) | Sind Lieferkettenstufen und ihre Reihenfolge darstellbar? | True |
| [CQ27](../queries/competency/CQ27.rq) | Trägt die Organisation eine Rolle statt die Anlage damit gleichzusetzen? | True |
| [CQ28](../queries/competency/CQ28.rq) | Bleibt eine Exposition vom realisierten Ausfall unterscheidbar? | True |
| [CQ29](../queries/competency/CQ29.rq) | Kann eine Maßnahme Risiko und zuständigen Akteur verbinden? | True |
| [CQ30](../queries/competency/CQ30.rq) | Ist eine PDL-Repräsentation von der physischen Anlage getrennt? | True |
| [CQ31](../queries/competency/CQ31.rq) | Bleiben Transportprozess und Versanddokument verschieden? | True |

## Transportnetz-Ergänzung rc3

Die ausdrücklich erfundene Datei `examples/current/transport-example.ttl` ergänzt die bisherigen Beispiele.

- CQ32: Sind die synthetischen Straßenreferenzpunkte durch eine berechnete Route verbunden?
- CQ33: Hat die hypothetische Brückensperrung einen längeren Umweg ohne gesperrtes Segment?
- CQ34: Sind Straßen- und Bahnrouten über gerichtete, routenspezifische Schritte nachvollziehbar?
