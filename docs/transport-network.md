# Transportprofil rc3: Infrastruktur, Topologie und Routen

Stand15.10.2026. Einstieg `ontology/current/profiles/transport.ttl`; Namespace unverändert `https://projekt-provider.de/ontology/`.

Die physischen Straßen-/Bahnobjekte liegen im Infrastrukturmodul. Ein `network:Segment` beschreibt einen topologischen Abschnitt und verweist über `representedAsset` auf das physische Objekt. Eine `Traversal` beschreibt eine gerichtete Nutzung dieses Abschnitts mit `fromJunction` und `toJunction`. Road-/Rail-Knoten bleiben getrennt; Ortsgleichheit ist kein Umschlag.

Eine `network:Route` ist eine informationelle Route im Kernmodell und nicht länger automatisch selbst ein Netz. `hasSegment` kann zu Netz oder Route gehören, ohne eine Route durch Domain-Inferenz wieder zum Netz zu machen. Das abstrakte `network:Network` ist eine PROV-Entity; es wird nicht auf das physische BFO-Netzaggregat verengt. Physische Transportinfrastruktur spezialisiert dagegen `core:InfrastructureAsset`.

`TransportPath` bezeichnet einen berechneten Kandidaten und spezialisiert `core:RouteEstimate`; keine beobachtete Fahrt. Jeder routenspezifische `RouteStep` bindet Traversierung, Segment, Reihenfolge und `stepRole`. Globale `routeSequence`, `routeRole`, `nextSegment` und `previousSegment` bleiben als veraltete Kompatibilität erhalten; sie sind keine ausreichende Grundlage für richtungsabhängiges Routing.

`ClosureScenario` bezeichnet einen ausdrücklich hypothetischen Segmentausschluss. Eine alternative Route wird neu berechnet und verknüpft dieses Szenario. Es wird kein realer Ausfall behauptet. Die SHACL-Prüfung kontrolliert Endpunkte, Modi, Schritte und den Ausschluss gesperrter Segmente.

Echtdatenpilot: begrenzter OSM-Ausschnitt Duisburg-Logport. Konverter, geprüfte Netzberechnung und Quellenbedingungen sind in provider-datasets/docs/transport-network.md dokumentiert. Die Workflow-Anbindung liegt in provider-workflow/docs/transport-network.md. Es gibt keine automatische Identitätsbestätigung von Werk, Terminal oder Hafen und kein vollständiges Lkw-/Zugprofil.

rc2 bleibt unter docs/review/2026-10-15/rc2/ gesichert. Die Berichte vom14.10. gelten unverändert für diesen Vorgängerstand; rc3 ergänzt den begrenzten Transportpiloten.

## Abnahme

34 Kompetenzfragen erfolgreich; 42 bestehende Tests plus drei Transport-Profiltests. OWL2-DL/HermiT mit dem gepinnten BFO-Kern erfolgreich. Synthetische Referenzanbindung, längerer Umweg bei hypothetischer Brückensperrung und gerichtete Straßen-/Bahnschritte werden durch CQ32–CQ34 geprüft; geometrische Kreuzungen, Zugangs-/Abbiegebeschränkungen und Richtungen zusätzlich im Datasets- und Workflow-Repository. Maschinenlesbare Nachweise: docs/review/2026-10-15/.
