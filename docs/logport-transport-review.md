# Reale Logport-Fachprüfung · 16.10.2026

Das Datasets-Dossier `reports/transport-logport/2026-10-16/` prüft das aktuelle Transportprofil0.3.0-rc3 an einem realen Regions-PBF. Zwei Terminalidentitäten sind über Betreibername und Anschrift gestützt, konkrete OSM-Torknoten bleiben unbestätigt. Vier berichtete Modus-Aussagen und vier Zugangskandidaten werden als `EvidenceAssertion` mit `Reported` bzw. `Modelled` und RDF-Reifikation dargestellt. Für Kandidaten wird keine direkte `infra:isConnectedTo`-Beziehung behauptet.

Die vorhandenen Klassen reichen dafür aus; kein Schema-/Releasewechsel erforderlich. Die SHACL-Prüfung des realen Netzes und fünf ausführbare SPARQL-Prüfungen stehen im Datasets-Dossier. Szenariosperrung bleibt `ScenarioAssumption`; Wege sind `TransportPath`/`Modelled`. Ein unter privaten Zugangsbeschränkungen oder an einer Barriere fehlender Weg widerlegt keinen berichteten Terminalanschluss.

Noch offene Fachbelege: aktuelle bestätigte Tor-/Gleisübergabestellen und begrenzte betriebliche Berechtigungsprofile. Erst daraus entstehende konkrete Kompetenzfragen können einen gezielten Schemaausbau begründen. Es gibt keine automatische Werkszuordnung, aktuelle Betriebsfreigabe oder pauschale öffentliche KG-Freigabe.
