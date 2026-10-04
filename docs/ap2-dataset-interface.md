# AP2: Ontologie-Schnittstelle zu Dataset-Artefakten

Entscheidung J1-04/J1-05, Stand 03.10.2026. Dieses Organisationsrepository bleibt autoritativ für Modelle und Shapes. Datenkonverter und Manifestvertrag werden in `PROVIDER-Project/provider-datasets` gepflegt; Akquise/Betrieb gehören zum gewählten Workflow.

## Verbindliche Baseline und URI-Grenzen

Core 0.2.0, Referenzcommit `ea060ca2f9f9a253947f6f66e572679ed8f0a75d`, Datei `ontology/provider-main.ttl`. Tatsächliche Core-Namespace: `http://projekt-provider.de/ontology/`; Supply-Chain: `http://projekt-provider.de/ontology/supply-chain#`. Diese Baseline wird nicht durch lokal unversionierte Dateien ersetzt. Insbesondere das lokale Eventmodul mit `https://w3id.org/provider/ontology/event#` ist Reviewmaterial und wird mit dieser Architekturentscheidung nicht freigegeben.

Graphnamen `https://w3id.org/provider/graph/<dataset-id>/<artifact-id>` sind logische Datenartefakt-Identitäten und keine neue Ontologie-Namespace. Synthetische Demonstrationen verwenden separate `example.org`-Graph-/Ressourcen-URIs. Bestehende SKOS/XKOS- und GDACS/GeoSPARQL-Quellen-URIs bleiben bis zu fachlich überprüften Mappings erhalten.

## Profilreferenz im Manifest

Dataset-Vertrag 1.0.0 führt Ontologieprofil-ID/-version, Core-Version und Referenzcommit sowie eine Konformitätsgrenze. Aktuelles Profil `provider-source-vocabularies` 1.0.0 ist **reference-only**: HS und GDACS bestehen fokussierte Konverterprüfungen, aber noch keine vollständige PROVIDER-Ontologie-/SHACL-Abnahme. Ein Baseline-Verweis ist kein Beweis, dass alle ausgegebenen Aussagen diese Ontologie benutzen oder erfüllen.

Änderungen an fachlichen Mappings oder Shapes benötigen eine neue Profil-/Mappingversion. Die konkrete Shape-Datei und deren SHA-256 gehören bei späterer SHACL-Abnahme in das neue Profil, statt ungeprüfte Shape-Versionen zu erfinden. Das Konvertermanifest ist unveränderlich; späteres Partnerreview/Freigabe referenziert separat Artefakt-ID und Dateichecksummen.

## Nachfolgende Modellarbeit

J1-07 konsolidiert Operational Port, Trade Location, Observation, Event/Episode, SourceRecord und MatchAssertion sowie Namespace-/ID-Regeln. J1-09 erstellt/pinnt Shapes und prüft absichtlich fehlerhafte Beispiele. GDACS-Episodenwerte werden im Dataset-Paket separat geführt; bestehende Domain-/Range-Angaben der lokalen Quellenvokabulare und die PROVIDER-Abbildung sind dabei explizit fachlich zu prüfen. Der ursprüngliche Architekturstand änderte keine Modell-Dateien. J1-07 ergänzt jetzt ein separates, explizit zuzuschaltendes Pilotprofil; der Core und bestehende Dataset-Manifeste bleiben erhalten. Details: [Modellprofil](ap2-pilot-profile.md) und [Profilreferenz](ap2-pilot-profile.json).

Autoritative Vertragserklärung: [provider-datasets](https://github.com/PROVIDER-Project/provider-datasets), `docs/artifact-contract.md`; Architektur: `docs/architecture.md`. Workflow-Verbraucher: [provider-workflow](https://github.com/PROVIDER-Project/provider-workflow), `docs/ap2-architecture.md`.
