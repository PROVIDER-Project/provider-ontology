# Aktive PROVIDER-Repositories

Stand: 06.10.2026. Die folgenden Remote-Branches wurden direkt auf GitHub geprüft.
Sie enthalten den gemeinsamen AP2-Arbeitsstand; `main` ist bei keinem der drei
Repositories die hier aufgeführte Arbeitsbaseline.

| Repository | Aktiver Remote-Branch | Geprüfter Arbeitscommit | Lokaler Checkout auf dem bisherigen Arbeitsrechner |
|---|---|---|---|
| [provider-datasets](https://github.com/PROVIDER-Project/provider-datasets/tree/ap2-local-progress) | `ap2-local-progress` | `e2b825803f21dde63c5f17ca315faeac4452bda1` | `ontologies/provider-datasets` |
| [provider-workflow](https://github.com/PROVIDER-Project/provider-workflow/tree/ap2-workflow-migration) | `ap2-workflow-migration` | `0facd954d7b5489ed62a6aa34bf060fdf9f9ff84` | `code/dagster-gdacs` |
| [provider-ontology](https://github.com/PROVIDER-Project/provider-ontology/tree/develop) | `develop` | `85df18ec15117db050df96f7d715dd4b18ce1796` | `ontologies/provider-ontology` |

Die Commit-IDs dokumentieren den geprüften Implementierungsstand vor dieser
Dokumentationskorrektur. Spätere Commits auf den Arbeitsbranches sind möglich;
reproduzierbare Laufpakete verwenden weiterhin ihre ausdrücklich gepinnten Versionen.

## Frischer Checkout

Aus einem gemeinsamen PROVIDER-Arbeitsverzeichnis mit GitHub-SSH-Zugriff:

```bash
mkdir -p ontologies code
git clone --branch ap2-local-progress git@github.com:PROVIDER-Project/provider-datasets.git ontologies/provider-datasets
git clone --branch ap2-workflow-migration git@github.com:PROVIDER-Project/provider-workflow.git code/dagster-gdacs
git clone --branch develop git@github.com:PROVIDER-Project/provider-ontology.git ontologies/provider-ontology
```

Die Befehle sind für neue, noch nicht vorhandene Zielverzeichnisse gedacht. Das
Layout erhält die dokumentierten relativen Pfade zwischen Workflow und Ontologie.
Die Installation und Startanleitung stehen im jeweiligen README; SSH-Zugriff allein
stellt noch keine Laufumgebung bereit.

## Lokale Branches und Remotes

- Datasets: lokal `main`, noch mit Upstream `origin/main`; der gesicherte AP2-Stand
  liegt auf `origin/ap2-local-progress`. Die getrennten Historien sind noch nicht
  zusammengeführt. Ein gewöhnlicher Push nach `main` ersetzt diese Zusammenführung nicht.
- Workflow: lokal `master`, Upstream `origin/ap2-workflow-migration`.
  `origin` ist `PROVIDER-Project/provider-workflow`; das bisherige persönliche
  Repository `LorenzBuehmann/provider-dagster` ist als `legacy` erhalten.
- Ontologie: lokal `develop`, Upstream `origin/develop`.

Der Workflow-Ordner heißt auf dem bisherigen Rechner weiterhin `code/dagster-gdacs`.
Eine Umbenennung zu `code/provider-workflow` ist noch nicht erfolgt. Pfadbeispiele
mit `dagster-gdacs` sind daher weiterhin gültig; vor einer Umbenennung müssen
betroffene Startkonfigurationen, Dienste und absolute Pfade angepasst werden.
Repository-Name und lokaler Verzeichnisname müssen nicht identisch sein.

## Umfang der Remote-Sicherung

Gesichert sind die committed Code-, Modell- und Dokumentationsstände einschließlich
Git-Historie. Nicht committed beziehungsweise ignorierte Rohdaten, generierte RDF,
Laufzustände, lokale Quellenkonfigurationen und Zugangsdaten werden nicht durch den
Push übertragen. Sie benötigen bei einem Rechnerwechsel die jeweiligen
Regenerations- oder Bereitstellungsschritte. Der Push ist kein Datenrelease und
ändert weder die Repository-Sichtbarkeit noch Quellenfreigaben.

Zusätzliche Arbeitsrepositories: `datasets/soy-backtest-filtered` hat lokal noch
einen Commit gegenüber dem zuletzt gespeicherten Remote-Stand; für
`datasets/provider-modern-searoute` ist noch kein Remote eingerichtet. `provider-pdl`
bleibt das bestehende autoritative Referenzrepository.
