"""Build the partner-facing ontology review PDF from its pinned review dossier."""
from pathlib import Path
import json,hashlib,html
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,Table,TableStyle,PageBreak
from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
ROOT=Path(__file__).resolve().parents[1]

def main():
 r=ROOT;folder=r/'reports/ontology-review/2026-10-13';folder.mkdir(parents=True,exist_ok=True)
 load=lambda p:json.loads((r/p).read_text())
 findings=load('docs/review/2026-10-13/findings.json')['findings'];coverage=load('docs/dataset-coverage.json')['sources'];questions=load('docs/competency-questions.json')['questions'];verification=load('docs/review/2026-10-13/verification.json')
 font=Path('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf');bold=font.with_name('DejaVuSans-Bold.ttf')
 if font.exists():pdfmetrics.registerFont(TTFont('Review',str(font)));pdfmetrics.registerFont(TTFont('ReviewBold',str(bold)));regular='Review';heavy='ReviewBold'
 else:regular='Helvetica';heavy='Helvetica-Bold'
 styles=getSampleStyleSheet();normal=ParagraphStyle('ReviewBody',fontName=regular,fontSize=9.5,leading=14,spaceAfter=10);title=ParagraphStyle('ReviewTitle',parent=normal,fontName=heavy,fontSize=21,leading=26,spaceAfter=16);heading=ParagraphStyle('ReviewHeading',parent=normal,fontName=heavy,fontSize=15,leading=20,spaceAfter=12);sub=ParagraphStyle('ReviewSub',parent=normal,fontName=heavy,fontSize=11,leading=16,spaceBefore=9,spaceAfter=6);small=ParagraphStyle('ReviewSmall',parent=normal,fontSize=8,leading=11,spaceAfter=0)
 def para(s,style=normal):return Paragraph(html.escape(str(s)),style)
 def table(headers,rows,widths):
  t=Table([[para(x,small) for x in row] for row in [headers]+rows],colWidths=widths,repeatRows=1,hAlign='LEFT');t.setStyle(TableStyle([('GRID',(0,0),(-1,-1),.35,colors.HexColor('#D4DEE3')),('BACKGROUND',(0,0),(-1,0),colors.HexColor('#DAE8EC')),('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,colors.HexColor('#F4F7F8')]),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),6),('RIGHTPADDING',(0,0),(-1,-1),6),('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5)]));return t
 story=[para('PROVIDER Ontologie-Review',title),para('InfAI | AP2 | 13.10.2026 | Modellkandidat 0.3.0-rc1'),para('Ergebnis und Verbindlichkeit',heading),para('Ein aktiver Modellstand mit dem Zielnamensraum https://projekt-provider.de/ontology/ ersetzt die bisher unklare Mischung aus HTTP, HTTPS, einer abweichenden CPPI-Domain und w3id-Entwürfen. Historische Profile bleiben überprüfbar; bestehende produktive Daten werden nicht still umgeschrieben.'),table(['Prüfbereich','Ergebnis'],[['Vorhandene RDF-Dateien','32 inventarisiert, einschließlich lokaler Entwürfe'],['Aktive Modellmodule','15 mit expliziten lokalen Imports und Hashes'],['Kompetenzfragen','31 ausführbare SPARQL-Fragen'],['Datasetregister','34 Einträge mit Modell- und Adapterzuordnung'],['Automatische Tests',str(verification['tests']['count'])+' Tests bestanden'],['Comext-Projektion','3960 Zellen; 1124 fehlend; vollständiges Statistik-SHACL bestanden']],[180,310]),para('Was jetzt besser ist',sub),para('Physische Waren sind von Klassifikationsbegriffen getrennt, Beobachtungsergebnisse von Aktivitäten und Quellenrecords von beschriebenen Anlagen. Fehlende Werte bleiben fehlend. Kennzahlart, Einheit, Klassifikationsversion und Zeitbezug sind explizit. Gefahrenmeldungen oder Szenarioannahmen erzeugen keinen unbelegten Ausfall.'),para('Prüfgrenze',sub),para('Lokaler Reviewkandidat; keine formale Partnerabnahme oder Veröffentlichung. Die Modellierbarkeit wird an synthetischen Beispielen geprüft. Der echte Comext-Ausschnitt ist vollständig gegen das Statistikprofil geprüft. Andere produktive Adapter sind noch separat zu migrieren. Vollständige externe BFO-Imports und vollständige OWL2-DL-Konsistenz sind nicht zertifiziert.')]
 story+=[PageBreak(),para('Befunde und Entscheidungen',heading)]
 for f in findings[:8]:story+=[para(f["id"]+' | '+f['problem'],sub),para(f['decision'])]
 for start in [0,17]:
  story += [PageBreak(),para('Abdeckung des Datenregisters '+('1/2' if start==0 else '2/2'),heading),para('Modellabdeckung bedeutet ausdrückliche Zuordnung der vorhandenen oder geplanten Quelle. Sie behauptet keine vollständige Datenintegration oder Nutzungsfreigabe.')]
  rows=[]
  for s in coverage[start:start+17]:
   status='Comext real projiziert und geprüft' if s['integration_status']=='comext-real-projection-validated' else ('Bestehendes Quellmodell; Adapter offen' if s['integration_status'].startswith('legacy') else 'Modell vorhanden; kein produktiver Adapter')
   rows.append([s['source_id'],'ausgewählt' if s['selection']=='selected' else 'zurückgestellt',status])
  story.append(table(['Quelle / Produkt','Auswahl','Modell- und Integrationsstand'],rows,[145,85,260]))
 for start in [0,16]:
  story += [PageBreak(),para('Kompetenzfragen '+('1/2' if start==0 else '2/2'),heading),para('Alle Fragen laufen gegen Schema und ausdrücklich erfundene Beispiele. Antworttabellen und negative Erwartungen sind Teil der Tests; sie sind keine empirischen Datenbefunde.')]
  rows=[[q['id'],q['question_de'],'Tabelle' if isinstance(q['expected'],list) else ('ja' if q['expected'] else 'nein')] for q in questions[start:start+16]];story.append(table(['ID','Prüffrage','Erwartung'],rows,[45,390,55]))
 story += [PageBreak(),para('Migration, Grenzen und nächste Arbeit',heading)]
 for f in findings[8:]:story += [para(f['id']+' | '+f['problem'],sub),para(f['decision'])]
 story += [para('Verbindlicher Einstieg',sub),para('ontology/current/provider.ttl; docs/current-release.json. Der lokale catalog-v001.xml ordnet Ontologie- und Versions-IRIs den Dateien zu. Die Prüftools laden ausschließlich Manifestdateien und führen keine Netzwerkimports aus.'),para('Nächste Umsetzung',sub),para('GENESIS gegen das Statistikmodell paketieren. Anschließend Producer und Workflow-Pins mit getrennten, versionierten Adaptern migrieren; zunächst Häfen/CPPI, dann Mining und Ereignisse. Fachliche Kompetenzfragen mit AP1 und Modellpartnern abstimmen.'),para('Nachweise und Standards',sub),para('docs/ontology-review.md; docs/competency-questions.json; docs/dataset-coverage.json; docs/review/2026-10-13/. W3C: https://www.w3.org/TR/owl2-primer/ und https://www.w3.org/TR/shacl/. Modullizenzen bleiben getrennt: Event-Entwurf CC BY4.0; weitere Module gemäß ihren MIT-Angaben. Keine daraus abgeleitete Lizenz für Quelldaten oder den gesamten KG.')]
 def footer(c,doc):c.setFont(regular,8);c.setFillColor(colors.HexColor('#526B78'));c.drawString(48,27,'PROVIDER | InfAI | Ontologie-Review | 13.10.2026');c.drawRightString(A4[0]-48,27,str(doc.page))
 target=folder/'PROVIDER_Ontologie_Review.pdf';doc=SimpleDocTemplate(str(target),pagesize=A4,leftMargin=48,rightMargin=48,topMargin=42,bottomMargin=43,title='PROVIDER Ontologie-Review',author='InfAI',invariant=1);doc.build(story,onFirstPage=footer,onLaterPages=footer)
 print(target)
if __name__=='__main__':main()
