from pathlib import Path
import csv
from datetime import datetime
from collections import defaultdict

from scripts.validate_data import validate_data

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "02_Data" / "processed"

def read_csv(name):
    with (DATA/name).open(encoding='utf-8') as f: return list(csv.DictReader(f))
def write_csv(path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows: rows=[{'message':'No records'}]
    with path.open('w', newline='', encoding='utf-8') as f:
        w=csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
def money(x): return round(float(x),2)
def month(s): return s[:7]
def date(s): return datetime.strptime(s,'%Y-%m-%d')
def group_sum(rows, key, val):
    d=defaultdict(float)
    for r in rows: d[r[key]] += float(r[val])
    return [{key:k, val:round(v,2)} for k,v in sorted(d.items())]
def md_table(rows):
    if not rows: return 'No records.'
    headers=list(rows[0].keys()); out=['| '+' | '.join(headers)+' |','| '+' | '.join(['---']*len(headers))+' |']
    for r in rows: out.append('| '+' | '.join(str(r.get(h,'')) for h in headers)+' |')
    return '\n'.join(out)
def svg_bar(path,title,labels,values):
    max_v=max(values) if values else 1; bw=600/max(len(values),1); parts=[f'<svg xmlns="http://www.w3.org/2000/svg" width="900" height="420" viewBox="0 0 900 420">','<rect width="100%" height="100%" fill="white"/>',f'<text x="30" y="35" font-family="Arial" font-size="22" font-weight="700">{title}</text>']
    for i,(l,v) in enumerate(zip(labels,values)):
        h=280*v/max_v; x=70+i*bw; y=350-h
        parts += [f'<rect x="{x:.1f}" y="{y:.1f}" width="{bw*.7:.1f}" height="{h:.1f}" fill="#2f6f9f"/>',f'<text x="{x:.1f}" y="372" font-family="Arial" font-size="11" transform="rotate(35 {x:.1f},372)">{l}</text>',f'<text x="{x:.1f}" y="{y-6:.1f}" font-family="Arial" font-size="10">{v:,.0f}</text>']
    parts.append('</svg>'); path.write_text('\n'.join(parts), encoding='utf-8')
def report(path,title,sections):
    txt=[f'# {title}','','Synthetic/anonymized SAP S/4HANA-inspired hospitality ERP analytics prototype.','']
    for h,b in sections: txt += [f'## {h}',b,'']
    path.write_text('\n'.join(txt), encoding='utf-8')


def main():
    validate_data()
    sales=read_csv('sales_revenue_clean.csv'); invoices=read_csv('customer_invoices_clean.csv'); payments=read_csv('customer_payments_clean.csv'); costs=read_csv('cost_center_budget_actual_clean.csv'); procure=read_csv('procurement_vendor_clean.csv'); inventory=read_csv('inventory_movements_clean.csv'); customers={r['customer_id']:r for r in read_csv('customers_clean.csv')}; vendors={r['vendor_id']:r for r in read_csv('vendors_clean.csv')}
    pay_by_inv=defaultdict(float)
    for p in payments: pay_by_inv[p['invoice_id']]+=float(p['payment_amount'])
    buckets=defaultdict(float)
    for inv in invoices:
        out=float(inv['invoice_amount'])-pay_by_inv[inv['invoice_id']]; days=max(0,(date('2025-12-31')-date(inv['due_date'])).days)
        b='Current' if days==0 else '1-30' if days<=30 else '31-60' if days<=60 else '61-90' if days<=90 else '90+'
        buckets[b]+=out
    ar=[{'aging_bucket':b,'outstanding_balance':round(buckets.get(b,0),2)} for b in ['Current','1-30','31-60','61-90','90+']]
    rev=defaultdict(float)
    for s in sales: rev[month(s['sale_date'])]+=float(s['net_revenue'])
    trend=[{'period':k,'net_revenue':round(v,2)} for k,v in sorted(rev.items())]
    coll=defaultdict(float)
    for p in payments: coll[month(p['payment_date'])]+=float(p['payment_amount'])
    collections=[{'period':k,'payment_amount':round(v,2)} for k,v in sorted(coll.items())]
    write_csv(ROOT/'03_FI_Module/outputs/ar_aging.csv',ar); write_csv(ROOT/'03_FI_Module/outputs/revenue_trend.csv',trend); write_csv(ROOT/'03_FI_Module/outputs/cash_collections.csv',collections); svg_bar(ROOT/'03_FI_Module/outputs/revenue_trend.svg','Monthly Net Revenue',[r['period'] for r in trend],[r['net_revenue'] for r in trend]); report(ROOT/'03_FI_Module/outputs/fi_report.md','FI Analysis Report',[('AR aging',md_table(ar)),('Revenue trend',md_table(trend[-6:])),('Cash collections',md_table(collections[-6:]))])
    cc=defaultdict(lambda:[0,0,''])
    for c in costs: cc[c['cost_center_id']][0]+=float(c['budget_amount']); cc[c['cost_center_id']][1]+=float(c['actual_amount']); cc[c['cost_center_id']][2]=c['cost_center_name']
    cc_rows=[{'cost_center_id':k,'cost_center_name':v[2],'budget_amount':round(v[0],2),'actual_amount':round(v[1],2),'variance':round(v[1]-v[0],2)} for k,v in sorted(cc.items())]
    total_rev=sum(float(s['net_revenue']) for s in sales); total_cost=sum(float(c['actual_amount']) for c in costs)
    profit=[{'metric':'Net revenue','amount':round(total_rev,2)},{'metric':'Operating cost','amount':round(total_cost,2)},{'metric':'Operating profit','amount':round(total_rev-total_cost,2)}]
    write_csv(ROOT/'04_CO_Module/outputs/cost_center_variance.csv',cc_rows); write_csv(ROOT/'04_CO_Module/outputs/profitability_summary.csv',profit); svg_bar(ROOT/'04_CO_Module/outputs/cost_center_actuals.svg','Actual Cost by Cost Center',[r['cost_center_name'] for r in cc_rows],[r['actual_amount'] for r in cc_rows]); report(ROOT/'04_CO_Module/outputs/co_report.md','CO Analysis Report',[('Budget vs actual',md_table(cc_rows)),('Profitability',md_table(profit))])
    cat=group_sum(sales,'revenue_category','net_revenue'); chan=group_sum(sales,'channel','net_revenue'); segd=defaultdict(float)
    for s in sales: segd[customers[s['customer_id']]['segment']]+=float(s['net_revenue'])
    seg=[{'segment':k,'net_revenue':round(v,2)} for k,v in sorted(segd.items(), key=lambda x:-x[1])]
    write_csv(ROOT/'05_SD_Module/outputs/revenue_by_category.csv',cat); write_csv(ROOT/'05_SD_Module/outputs/revenue_by_channel.csv',chan); write_csv(ROOT/'05_SD_Module/outputs/customer_segment_revenue.csv',seg); svg_bar(ROOT/'05_SD_Module/outputs/revenue_by_channel.svg','Revenue by Sales Channel',[r['channel'] for r in chan],[r['net_revenue'] for r in chan]); report(ROOT/'05_SD_Module/outputs/sd_report.md','SD Analysis Report',[('Revenue by category',md_table(cat)),('Revenue by channel',md_table(chan)),('Customer segments',md_table(seg))])
    spend=group_sum(procure,'category','purchase_amount'); vd=defaultdict(lambda:[0,0,0,''])
    for p in procure:
        delay=(date(p['received_date'])-date(p['promised_date'])).days; v=vd[p['vendor_id']]; v[0]+=float(p['purchase_amount']); v[1]+=delay; v[2]+=1; v[3]=vendors[p['vendor_id']]['vendor_name']
    vendor_rows=[{'vendor_id':k,'vendor_name':v[3],'purchase_amount':round(v[0],2),'avg_delivery_delay_days':round(v[1]/v[2],2),'on_time_delivery_pct':vendors[k]['on_time_delivery_pct']} for k,v in sorted(vd.items())]
    reorder=[{k:r[k] for k in ['period','item_id','item_name','closing_stock','reorder_point']} for r in inventory if float(r['closing_stock'])<=float(r['reorder_point'])]
    write_csv(ROOT/'06_MM_Module/outputs/purchase_spend.csv',spend); write_csv(ROOT/'06_MM_Module/outputs/vendor_performance.csv',vendor_rows); write_csv(ROOT/'06_MM_Module/outputs/reorder_alerts.csv',reorder); svg_bar(ROOT/'06_MM_Module/outputs/purchase_spend.svg','Purchase Spend by Category',[r['category'] for r in spend],[r['purchase_amount'] for r in spend]); report(ROOT/'06_MM_Module/outputs/mm_report.md','MM Analysis Report',[('Purchase spend',md_table(spend)),('Vendor performance',md_table(vendor_rows)),('Reorder alerts',md_table(reorder[:20]))])
    y=[r['net_revenue'] for r in trend]; slope=(y[-3]-y[0])/(len(y)-3); intercept=y[0]
    forecast=[]
    for i,r in enumerate(trend):
        pred=round(intercept+slope*i,2); forecast.append({'period':r['period'],'net_revenue':r['net_revenue'],'forecast_revenue':pred,'absolute_error':round(abs(r['net_revenue']-pred),2)})
    hold=forecast[-2:]; mape=round(sum(h['absolute_error']/h['net_revenue'] for h in hold)/len(hold)*100,2)
    cash=[]; vals=[r['payment_amount'] for r in collections]
    for i,r in enumerate(collections): cash.append({'period':r['period'],'payment_amount':r['payment_amount'],'forecast_cash_collection':round(sum(vals[max(0,i-3):i] or [vals[0]])/len(vals[max(0,i-3):i] or [vals[0]]),2)})
    metrics=[{'model':'Revenue linear trend baseline','holdout_months':2,'mape_pct':mape,'mae':round(sum(h['absolute_error'] for h in hold)/2,2)},{'model':'Cash collection 3-month moving average','holdout_months':0,'mape_pct':'n/a','mae':'n/a'}]
    write_csv(ROOT/'07_Analytics_Forecasting/outputs/revenue_forecast.csv',forecast); write_csv(ROOT/'07_Analytics_Forecasting/outputs/cash_flow_forecast.csv',cash); write_csv(ROOT/'07_Analytics_Forecasting/outputs/forecast_metrics.csv',metrics); svg_bar(ROOT/'07_Analytics_Forecasting/outputs/revenue_forecast.svg','Revenue Forecast Baseline',[r['period'] for r in forecast],[r['forecast_revenue'] for r in forecast]); report(ROOT/'07_Analytics_Forecasting/outputs/forecast_report.md','Analytics and Forecasting Report',[('Baseline forecasting approach','This report uses simple baseline methods for portfolio demonstration: a linear revenue trend baseline and a 3-month moving average for cash collections. It is not a production-grade predictive model and should not be used for operational commitments without a longer history, external demand drivers, and formal model monitoring.'),('Revenue forecast',md_table(forecast[-6:])),('Evaluation metrics','MAPE (Mean Absolute Percentage Error) shows average absolute forecast error as a percentage of actual revenue for the holdout months. MAE (Mean Absolute Error) shows the average absolute currency-unit error. Because the dataset is synthetic and short, these metrics are directional only and should not be interpreted as proof of reliable future accuracy.\n\n'+md_table(metrics)),('Cash-flow forecast',md_table(cash[-6:]))])
    kpis=[{'kpi':'Total net revenue','value':round(total_rev,2)},{'kpi':'Open AR balance','value':round(sum(r['outstanding_balance'] for r in ar),2)},{'kpi':'Operating profit','value':round(total_rev-total_cost,2)},{'kpi':'Purchase spend','value':round(sum(float(p['purchase_amount']) for p in procure),2)},{'kpi':'Reorder alerts','value':len(reorder)}]
    write_csv(ROOT/'09_Documentation/kpi_summary.csv',kpis); (ROOT/'09_Documentation/kpi_summary.md').write_text('# KPI Summary\n\n'+md_table(kpis)+'\n', encoding='utf-8')
    html="<!doctype html><html><head><meta charset='utf-8'><title>Hospitality ERP Analytics Dashboard</title><style>body{font-family:Arial;margin:32px;color:#1f2937}.grid{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}.card{border:1px solid #ddd;border-radius:8px;padding:16px}iframe{width:100%;height:430px;border:0}</style></head><body><h1>Hospitality ERP Analytics Dashboard</h1><p>Synthetic SAP S/4HANA-inspired prototype. All visuals are text-based SVG files.</p><div class='grid'>" + ''.join(f"<div class='card'><strong>{r['kpi']}</strong><br>{r['value']}</div>" for r in kpis) + "</div><h2>Charts</h2><iframe src='../../03_FI_Module/outputs/revenue_trend.svg'></iframe><iframe src='../../05_SD_Module/outputs/revenue_by_channel.svg'></iframe><iframe src='../../06_MM_Module/outputs/purchase_spend.svg'></iframe></body></html>"
    (ROOT/'08_BI_Integration/dashboard/index.html').write_text(html, encoding='utf-8')
if __name__=='__main__': main()
