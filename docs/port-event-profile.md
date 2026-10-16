# Grobe Ereignisse und Hafenbezug · 16.10.2026

Aktiver Arbeitsstand: [Optionales Hafenereignisprofil 0.1.0](../profiles/port-events/0.1.0/README.md). Es bindet den unveränderten Kandidaten 0.3.0-rc3, unterscheidet Quellenbefund, Umfang und Zeitqualität und benötigt keine OSM-Topologie. Die bestehenden Schema-Releases und historischen Artefakte bleiben unverändert.

Die bisherigen Logport-Detailanalysen bleiben für gezielte Erreichbarkeitsfragen nutzbar. Der nächste Projektpfad baut dagegen auf wenigen realen Meldungen und groben Zielreferenzen auf. Registerzuordnung und bedingte Funktionsfolgen liegen inzwischen als getrennte, gepinnte Datasets-Artefakte vor. Ihr Anschluss liegt im Workflow-Repository als manueller Job `port_event_review_job` mit vier Stufen und separaten Laufordnern vor. Die standardmäßigen historischen Reviewfälle werden offline verarbeitet; es werden keine heutigen Betriebszustände oder neuen Quellenfreigaben erzeugt. Keine pauschale Zuordnung von Unternehmensgruppenfolgen zu einem Hafen und keine Aufwertung von Exposition zur Betriebsunterbrechung.

Die Verwendung von `PossibleImpact` mit ausdrücklich unbestätigten Abhängigkeiten ist in [Bedingte Wirkungen](port-event-effects.md) beschrieben. Sie erfordert keine Änderung des Profilmanifests oder des Basismodells.
