from pathlib import Path
import csv,json
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, KeepTogether
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics

root=Path(r'C:/Users/Ruben Cuadrado/Documents/Codex/2026-10-31/es/outputs/Explorador_Recaudo_Tributario')
out=Path(r'C:/Users/Ruben Cuadrado/Documents/Codex/2026-10-31/es/outputs/Explorador_Recaudo_Tributario_hito2.pdf')
inv=json.loads((root/'results/data_inventory.json').read_text(encoding='utf-8'))
summary=json.loads((root/'results/baseline_summary.json').read_text(encoding='utf-8'))
with (root/'results/ranking_seccionales_2025.csv').open(encoding='utf-8-sig',newline='') as f: ranking=list(csv.DictReader(f))
with (root/'results/annual_comparison_2024_2025.csv').open(encoding='utf-8-sig',newline='') as f: annual_rows=list(csv.DictReader(f))
annual_2025={r['tax']:float(r['value_millions']) for r in annual_rows if r['year']=='2025'}
top=summary['top_alerts'][0]
styles=getSampleStyleSheet()
styles.add(ParagraphStyle(name='KickerX',parent=styles['Normal'],fontName='Helvetica-Bold',fontSize=8,textColor=colors.HexColor('#187C80'),leading=10,spaceAfter=5))
styles.add(ParagraphStyle(name='TitleX',parent=styles['Title'],fontName='Helvetica-Bold',fontSize=21,leading=24,textColor=colors.HexColor('#172B3A'),alignment=TA_LEFT,spaceAfter=4))
styles.add(ParagraphStyle(name='SubX',parent=styles['Normal'],fontName='Helvetica',fontSize=9,leading=12,textColor=colors.HexColor('#536371'),spaceAfter=8))
styles.add(ParagraphStyle(name='HeadX',parent=styles['Heading2'],fontName='Helvetica-Bold',fontSize=10.5,leading=13,textColor=colors.HexColor('#172B3A'),spaceBefore=7,spaceAfter=4))
styles.add(ParagraphStyle(name='BodyX',parent=styles['BodyText'],fontName='Helvetica',fontSize=8.3,leading=11,textColor=colors.HexColor('#233443'),spaceAfter=4))
styles.add(ParagraphStyle(name='SmallX',parent=styles['BodyText'],fontName='Helvetica',fontSize=7.4,leading=9.2,textColor=colors.HexColor('#465562'),spaceAfter=2))
styles.add(ParagraphStyle(name='MetricX',parent=styles['Normal'],fontName='Helvetica-Bold',fontSize=13,leading=15,textColor=colors.HexColor('#172B3A'),alignment=TA_LEFT))
styles.add(ParagraphStyle(name='MetricLabelX',parent=styles['Normal'],fontName='Helvetica',fontSize=7.2,leading=9,textColor=colors.HexColor('#536371')))

def P(text,style='BodyX'): return Paragraph(text,styles[style])
def million_fmt(x): return f"${float(x):,.1f} millones".replace(',','X').replace('.',',').replace('X','.')

doc=SimpleDocTemplate(str(out),pagesize=letter,rightMargin=0.55*inch,leftMargin=0.55*inch,topMargin=0.42*inch,bottomMargin=0.42*inch,title='Hito 2 - Explorador del recaudo tributario',author='Equipo del proyecto')
story=[]
story += [P('PROYECTO FINAL DE INTELIGENCIA ARTIFICIAL  |  HITO 2  |  14 NOVIEMBRE 2026','KickerX'),P('Explorador inteligente del recaudo tributario','TitleX'),P('Avance: datos preparados, línea base ejecutable y primer resultado guardado en el repositorio. Equipo e integrantes: completar antes de entregar.','SubX')]
metrics=[
 [P(f"{inv['monthly_tax_categories']}",'MetricX'),P(f"{summary['records_scored']}" ,'MetricX'),P(f"{inv['seccionales']}" ,'MetricX')],
 [P('categorías conservadas en la serie mensual (2000-sep. 2026)','MetricLabelX'),P('casos evaluados por la línea base en años completos (2006-2025)','MetricLabelX'),P('nombres de seccionales en la base anual (2005-sep. 2026)','MetricLabelX')]
]
t=Table(metrics,colWidths=[2.3*inch,2.3*inch,2.3*inch],rowHeights=[0.27*inch,0.42*inch])
t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),colors.HexColor('#F2F6F7')),('BOX',(0,0),(-1,-1),0.5,colors.HexColor('#D7E0E3')),('INNERGRID',(0,0),(-1,-1),0.5,colors.HexColor('#D7E0E3')),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),9),('RIGHTPADDING',(0,0),(-1,-1),8),('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),4)]))
story += [t,P('Qué está listo','HeadX'),P(f"Se prepararon {inv['annual_records']} registros nacionales anuales ({inv['annual_years'][0]}-sep. {inv['annual_years'][1]}), {inv['monthly_records']} filas mensuales nacionales con {inv['monthly_tax_categories']} categorías y {inv['territorial_records']:,} observaciones por seccional. La base territorial incluye {inv['seccionales']} seccionales y {inv['territorial_tax_categories']} categorías. Los valores están en millones de pesos corrientes. Los datos mensuales son nacionales; el archivo territorial es anual. La seccional reportada no debe interpretarse automáticamente como la ciudad donde se originó el recaudo.",'BodyX'),P('Línea base y primer resultado','HeadX'),P('Para este primer baseline se seleccionaron Renta total e IVA interno. Compara cada mes con los valores históricos del mismo mes calendario, usando la mediana y la desviación absoluta mediana (MAD) de años anteriores. Empieza a evaluar al tener seis años previos y marca una señal cuando la desviación robusta absoluta es al menos 3,5. Se excluye 2026 de esta primera comparación porque solo llega a septiembre y es preliminar.','BodyX')]
first=P(f"Señal de mayor puntuación: {top['tax']} en {top['month']} de {top['year']} = {million_fmt(top['value_millions'])}; mediana de los {top['prior_years']} valores previos disponibles para ese mes = {million_fmt(top['historical_median_millions'])}; puntuación robusta = {top['robust_z_score']}. En total, la línea base marcó {summary['alerts_count']} señales entre {summary['records_scored']} observaciones evaluadas. Es una alerta estadística exploratoria, no una explicación causal ni evidencia de irregularidad.",'BodyX')
story.append(first)
story += [P('Consulta anual de referencia (2025, año completo)','HeadX'),P(f"Renta y complementarios: {million_fmt(annual_2025['Renta y complementarios'])}; IVA interno: {million_fmt(annual_2025['IVA actividad interna'])}; IVA externo: {million_fmt(annual_2025['IVA actividad externa'])}; IVA combinado: {million_fmt(annual_2025['IVA total (interno + externo)'])}. Valores en millones de pesos corrientes, sin ajuste por inflación.",'BodyX')]
if len(ranking)>=2:
    story += [P('Primer resumen territorial (2025, año completo)','HeadX'),P(f"Mayor total registrado: {ranking[0]['seccional']} ({million_fmt(ranking[0]['value_millions'])}); siguiente: {ranking[1]['seccional']} ({million_fmt(ranking[1]['value_millions'])}). Se conserva el nombre de la dirección seccional tal como aparece en la fuente DIAN; esto no es un ranking de recaudo atribuible a ciudades.",'BodyX')]
story += [P('Primeras entradas de bitácora humano-IA','HeadX'),P('<b>11/11/2026 · ChatGPT (Codex):</b> ayudó a revisar periodos, categorías y granularidad de las fuentes. Propuesta provisional: separar el análisis mensual nacional del territorial anual; se descartaron alertas mensuales por ciudad porque el archivo no tiene ese nivel temporal. Confirmación del equipo pendiente. Verificación: inspección de encabezados, filas, cobertura y notas de los tres archivos DIAN. Integrante: completar.','SmallX'),P('<b>11/11/2026 · ChatGPT (Codex):</b> apoyó la preparación de datos y la ejecución de la primera línea base mediana/MAD. Se propone usarla como línea base sujeta a revisión del equipo; 2026 parcial queda fuera del puntaje inicial. Verificación: scripts reproducibles y archivos de resultado en el repositorio. Integrante: completar.','SmallX'),P('<b>14/11/2026 · ChatGPT (Codex):</b> amplió la tabla mensual para conservar todas las categorías numéricas; la línea base se mantuvo en Renta e IVA interno. Verificación: categorías comparadas con encabezados y nueva ejecución de ambos scripts. Integrante: completar.','SmallX'),P('Siguiente paso: revisar las señales con contexto tributario, contrastar otro método de detección y documentar preguntas de evaluación. La bitácora contiene una reflexión sobre el ajuste de alcance; cada integrante debe revisar y completar sus contribuciones.','SmallX')]

def footer(canvas,doc):
    canvas.saveState(); canvas.setStrokeColor(colors.HexColor('#D7E0E3')); canvas.line(doc.leftMargin,0.34*inch,letter[0]-doc.rightMargin,0.34*inch)
    canvas.setFont('Helvetica',6.5); canvas.setFillColor(colors.HexColor('#6B7780'))
    canvas.drawString(doc.leftMargin,0.22*inch,'Fuentes: archivos de estadísticas de recaudo DIAN proporcionados por el equipo; corte reportado: 23-oct-2026.')
    canvas.drawRightString(letter[0]-doc.rightMargin,0.22*inch,'Proyecto académico · resultados exploratorios')
    canvas.restoreState()
doc.build(story,onFirstPage=footer)
print(out)
print('alerts',summary['alerts_count'],'top',top['year'],top['month'],top['tax'],top['robust_z_score'],'ranking',ranking[:2])

