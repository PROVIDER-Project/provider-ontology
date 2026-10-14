# Granularität und Konsolidierungsentscheidungen – 14.10.2026

Die maschinelle Bestandsaufnahme erfasst alle lokal deklarierten Klassen und Eigenschaften des rc1. Sie trennt tatsächlich in Beispielen/Kompetenzfragen verwendete Begriffe, nur im Quellenregister zugeordnete Begriffe, bisher nicht geprüfte Erweiterungen und veraltete Kompatibilitätsbegriffe. Keine Löschung allein aufgrund fehlender Beispielverwendung.

## Entscheidungen

1. Gemeinsame Informationsergebnisse, Messwerte, Einheiten und Quellenbelege bilden den stabilen Kern. Domäneneigenschaften werden an diesen angeschlossen; Quellengraphen bleiben unverändert.
2. GENESIS/Comext benötigen Zellen, fehlende Werte, Klassifikation, Referenzperiode, Indexbasis, Produktionsumfang und Qualitätsmarker. Keine zusätzliche Klasse pro Tabelle, Produktcode oder Jahr.
3. Hafen-, CPPI- und Mining-Beobachtungen bleiben fachlich unterscheidbar, verwenden aber dasselbe Messwertmuster. Ein Indexwert ist weder Produktionsmenge noch physische Kapazität.
4. OSM-Infrastruktur beschreibt Anlagen und Geometrie. Sie belegt weder Betreiberidentität noch Kapazität, Ausfall oder Warenfluss ohne zusätzliche Quellen.
5. Mining-Anlagen, Unternehmen, Materialien und qualifizierte Zuordnungen bleiben getrennt. Kandidaten, Teil-von-Beziehungen und bestätigte Identität dürfen nicht zusammenfallen.
6. Ereignis, Gefährdung, realisierte Störung und Szenarioannahme bleiben getrennt. Die feineren Event- und Supply-Chain-Erweiterungen sind optional; nicht vollständig durch Echtdaten abgenommen.
7. BFO wird explizit optional. Der große integrierte Einstieg bleibt für Gesamtprüfungen, schlanke Einstiegspunkte begrenzen die benötigten Importmodule.
8. Literalbasierte historische Einheiten und veraltete Akteursrollen bleiben kompatibel, werden aber nicht als Muster für neue Daten empfohlen.

## Grenze

Das Register begründet Verwendungsumfang und Priorität, nicht die fachliche Wahrheit aller Definitionen. Fachpartner müssen insbesondere tatsächliche Störungen, Kapazitätsbasis, Matching-Entscheidungen und Szenarioannahmen prüfen. Die folgende Konsolidierung wird durch separate Modell-, Logik- und Echtdatenprüfungen belegt.
