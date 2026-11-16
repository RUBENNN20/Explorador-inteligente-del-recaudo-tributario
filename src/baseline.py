from pathlib import Path
import csv, json, math, statistics
ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/'data'/'processed'/'recaudo_mensual_nacional.csv'
OUT=ROOT/'results'/'baseline_alerts.csv'
MONTHS={'Enero':1,'Febrero':2,'Marzo':3,'Abril':4,'Mayo':5,'Junio':6,'Julio':7,'Agosto':8,'Septiembre':9,'Octubre':10,'Noviembre':11,'Diciembre':12}
MIN_HISTORY=6
ROBUST_Z_THRESHOLD=3.5
BASELINE_TAXES={'Renta total','IVA interno'}

def robust_score(value, history):
    med=statistics.median(history)
    mad=statistics.median([abs(x-med) for x in history])
    if mad > 0: return (value-med)/(1.4826*mad),med,mad
    # If history is constant, any nonzero difference is noteworthy, but avoid
    # division by zero and report the raw difference as the score.
    return (0.0 if value==med else math.copysign(float('inf'),value-med)),med,mad

with SOURCE.open(encoding='utf-8-sig',newline='') as f:
    rows=list(csv.DictReader(f))
series={}
for r in rows:
    if r['tax'] not in BASELINE_TAXES: continue
    year=int(r['year']); month=MONTHS.get(r['month'])
    if not month: continue
    series.setdefault((r['tax'],month),[]).append((year,float(r['value_millions']),r['month']))
alerts=[]
for (tax,month),items in series.items():
    items.sort()
    history=[]
    for year,value,label in items:
        # 2026 is year-to-date through September, so exclude it from comparable
        # complete-year baseline outputs. Future months do not affect any score.
        if year>2025: continue
        if len(history)>=MIN_HISTORY:
            score,med,mad=robust_score(value,[x[1] for x in history])
            if abs(score)>=ROBUST_Z_THRESHOLD:
                alerts.append({'year':year,'month':label,'tax':tax,'value_millions':round(value,3),'historical_median_millions':round(med,3),'historical_mad_millions':round(mad,3),'robust_z_score':('INF' if math.isinf(score) else round(score,3)),'prior_years':len(history),'baseline':'same calendar month, prior years only'})
        history.append((year,value,label))
alerts.sort(key=lambda x: (float('inf') if x['robust_z_score']=='INF' else abs(float(x['robust_z_score']))),reverse=True)
with OUT.open('w',encoding='utf-8-sig',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(alerts[0].keys()) if alerts else ['year','month','tax','value_millions','historical_median_millions','historical_mad_millions','robust_z_score','baseline'])
    w.writeheader();w.writerows(alerts)
summary={'method':'same-month historical median and MAD; prior years only','minimum_prior_years':MIN_HISTORY,'threshold_abs_robust_z':ROBUST_Z_THRESHOLD,'analysis_years':'2000-2025; partial 2026 excluded','baseline_taxes':sorted(BASELINE_TAXES),'records_scored':sum(max(0,min(2025,max(y for y,_,_ in a))-min(y for y,_,_ in a)+1-MIN_HISTORY) for a in series.values()),'alerts_count':len(alerts),'top_alerts':alerts[:10],'interpretation':'Exploratory statistical flags only; not causal explanations, tax audit findings, or proof of fraud.'}
(ROOT/'results'/'baseline_summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(summary,ensure_ascii=False,indent=2))
