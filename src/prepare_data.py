from pathlib import Path
import csv, io, json, math, re, statistics, zipfile, xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / 'data' / 'raw'
OUT = ROOT / 'data' / 'processed'
NS = {'m':'http://schemas.openxmlformats.org/spreadsheetml/2006/main', 'r':'http://schemas.openxmlformats.org/officeDocument/2006/relationships'}

def open_workbook(path):
    outer = zipfile.ZipFile(path)
    if path.suffix.lower() == '.zip':
        inner_name = next(n for n in outer.namelist() if n.lower().endswith('.xlsx'))
        z = zipfile.ZipFile(io.BytesIO(outer.read(inner_name)))
    else:
        z = outer
    strings = []
    if 'xl/sharedStrings.xml' in z.namelist():
        root = ET.fromstring(z.read('xl/sharedStrings.xml'))
        strings = [''.join(t.text or '' for t in si.findall('.//m:t',NS)) for si in root.findall('m:si',NS)]
    wb = ET.fromstring(z.read('xl/workbook.xml'))
    rel = ET.fromstring(z.read('xl/_rels/workbook.xml.rels'))
    targets = {x.attrib['Id']: x.attrib['Target'] for x in rel}
    sheet = wb.find('m:sheets/m:sheet',NS)
    target = targets[sheet.attrib['{'+NS['r']+'}id']].lstrip('/')
    sheet_path = target if target.startswith('xl/') else 'xl/'+target
    root = ET.fromstring(z.read(sheet_path))
    rows = []
    for row in root.findall('.//m:sheetData/m:row',NS):
        cells = {}
        for c in row.findall('m:c',NS):
            ref = c.attrib.get('r','')
            col = re.match(r'[A-Z]+',ref).group(0)
            v = c.find('m:v',NS)
            val = v.text if v is not None else ''
            if c.attrib.get('t') == 's' and val: val = strings[int(val)]
            elif c.attrib.get('t') == 'inlineStr': val = ''.join(t.text or '' for t in c.findall('.//m:t',NS))
            cells[col] = val
        rows.append(cells)
    return rows

def number(v):
    try:
        x=float(v)
        return x if math.isfinite(x) else None
    except (TypeError,ValueError): return None

def write_csv(path, fields, rows):
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open('w',newline='',encoding='utf-8-sig') as f:
        w=csv.DictWriter(f,fieldnames=fields); w.writeheader(); w.writerows(rows)


annual_file = next(RAW.glob('Recaudo-anual*.zip'))
annual_rows = open_workbook(annual_file)
annual_header = next(r for r in annual_rows if (r.get('B') or '').strip().upper()=='ACTIVIDAD INTERNA')
annual=[]
for row in annual_rows:
    year_text=(row.get('A') or '').strip()
    year=int(year_text[:4]) if year_text[:4].isdigit() else number(year_text)
    if year is None or not (1900 <= year <= 2100): continue
    for col,label in annual_header.items():
        if col=='A' or not label or label.strip().startswith(('I.','II.','III.','IV.')): continue
        value=number(row.get(col))
        if value is not None:
            annual.append({'year':int(year),'tax':label.strip(),'value_millions':round(value,6)})
write_csv(OUT/'recaudo_anual_nacional.csv',['year','tax','value_millions'],annual)
annual_selected={'Renta y complementarios /1':'Renta y complementarios','IVA /4':'IVA actividad interna','IVA':'IVA actividad externa'}
annual_reference=[{'year':r['year'],'tax':annual_selected[r['tax']],'value_millions':r['value_millions']} for r in annual if r['year'] in (2024,2025) and r['tax'] in annual_selected]
for y in (2024,2025):
    vals={r['tax']:r['value_millions'] for r in annual_reference if r['year']==y}
    vals['IVA total (interno + externo)']=round(vals['IVA actividad interna']+vals['IVA actividad externa'],6)
    annual_reference.extend({'year':y,'tax':tax,'value_millions':value} for tax,value in vals.items() if tax=='IVA total (interno + externo)')
write_csv(ROOT/'results'/'annual_comparison_2024_2025.csv',['year','tax','value_millions'],annual_reference)

monthly_file = next(RAW.glob('Recaudo-mensual*.zip'))
rows = open_workbook(monthly_file)
header = next(r for r in rows if r.get('A') == 'Año' and r.get('B') == 'Mes')

metric_cols={col:label.strip() for col,label in header.items() if col not in ('A','B') and label}
metric_cols['D']='Renta total'
metric_cols['G']='IVA interno'
monthly=[]
for row in rows:
    year=number(row.get('A')); month=(row.get('B') or '').strip()
    if year is None or month not in {'Enero','Febrero','Marzo','Abril','Mayo','Junio','Julio','Agosto','Septiembre','Octubre','Noviembre','Diciembre'}: continue
    for col,tax in metric_cols.items():
        value=number(row.get(col))
        if value is not None:
            monthly.append({'year':int(year),'month':month,'tax':tax,'value_millions':round(value,6)})
write_csv(OUT/'recaudo_mensual_nacional.csv',['year','month','tax','value_millions'],monthly)

territorial_file = next(RAW.glob('Recaudo-bruto-por-seccionales*.xlsx'))
rows = open_workbook(territorial_file)
head_idx = next(i for i,r in enumerate(rows) if (r.get('A') or '').strip().upper()=='AÑO' and 'SECCIONAL' in (r.get('B') or '').upper())
header = rows[head_idx]
territorial=[]
current_year=None
for row in rows[head_idx+1:]:
    year_text=(row.get('A') or '').strip()
    if year_text[:4].isdigit(): current_year=int(year_text[:4])
    year=current_year; section=(row.get('B') or '').strip()
    if year is None or not section or section.upper().startswith('TOTAL'): continue
    if not (2000 <= year <= 2100): continue
    for col,label in header.items():
        if col in ('A','B') or not label or label.strip().startswith('('): continue
        value=number(row.get(col))
        if value is None: continue
        territorial.append({'year':int(year),'seccional':section,'tax':label.strip(),'value_millions':round(value,6)})
write_csv(OUT/'recaudo_anual_seccional.csv',['year','seccional','tax','value_millions'],territorial)
ranked=[r for r in territorial if r['year']==2025 and r['tax'].upper().startswith('TOTAL')]
ranked.sort(key=lambda r:r['value_millions'],reverse=True)
write_csv(ROOT/'results'/'ranking_seccionales_2025.csv',['year','seccional','tax','value_millions'],ranked)

summary={'annual_records':len(annual),'annual_years':[min(x['year'] for x in annual),max(x['year'] for x in annual)] if annual else [],'annual_tax_categories':len(set(x['tax'] for x in annual)),'monthly_records':len(monthly),'monthly_years':[min(x['year'] for x in monthly),max(x['year'] for x in monthly)] if monthly else [],'monthly_taxes':sorted(set(x['tax'] for x in monthly)),'monthly_tax_categories':len(set(x['tax'] for x in monthly)),'territorial_records':len(territorial),'territorial_years':[min(x['year'] for x in territorial),max(x['year'] for x in territorial)] if territorial else [],'seccionales':len(set(x['seccional'] for x in territorial)),'territorial_tax_categories':len(set(x['tax'] for x in territorial))}
(ROOT/'results'/'data_inventory.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(summary,ensure_ascii=False,indent=2))







