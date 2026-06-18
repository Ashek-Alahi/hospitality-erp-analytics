from __future__ import annotations
from collections import defaultdict
from pathlib import Path
from scripts.reporting.common import md_table, write_csv


def calculate_vendor_performance(procurement, vendors, parse_date):
    stats=defaultdict(lambda:[0.0,0,0,0,""])
    for row in procurement:
        delay=max(0,(parse_date(row["received_date"])-parse_date(row["promised_date"])).days); s=stats[row["vendor_id"]]; s[0]+=float(row["purchase_amount"]); s[1]+=delay; s[2]+=1; s[3]+=1 if delay>0 else 0; s[4]=vendors[row["vendor_id"]]["vendor_name"]
    return [{"vendor_id":k,"vendor_name":v[4],"purchase_amount":round(v[0],2),"avg_delivery_delay_days":round(v[1]/v[2],2),"vendor_delay_rate_pct":round(v[3]/v[2]*100,2),"on_time_delivery_pct":round((v[2]-v[3])/v[2]*100,2)} for k,v in sorted(stats.items())]

def calculate_reorder_alerts(inventory):
    rows=[]
    for row in inventory:
        gap=round(float(row["reorder_point"])-float(row["closing_stock"]),2)
        if gap>=0:
            rows.append({"period":row["period"],"item_id":row["item_id"],"item_name":row["item_name"],"category":row["category"],"closing_stock":row["closing_stock"],"reorder_point":row["reorder_point"],"stock_gap":gap})
    return rows

def calculate_inventory_risk_summary(reorder):
    stats=defaultdict(lambda:{"alert_count":0,"items":set(),"lowest":None,"gaps":[]})
    for r in reorder:
        s=stats[r["category"]]; gap=float(r["stock_gap"]); closing=float(r["closing_stock"]); s["alert_count"]+=1; s["items"].add(r["item_id"]); s["lowest"]=closing if s["lowest"] is None else min(s["lowest"],closing); s["gaps"].append(gap)
    return [{"category":cat,"alert_count":s["alert_count"],"items_at_risk":len(s["items"]),"lowest_closing_stock":round(s["lowest"],2),"average_stock_gap":round(sum(s["gaps"])/len(s["gaps"]),2),"max_stock_gap":round(max(s["gaps"]),2)} for cat,s in sorted(stats.items(), key=lambda x:(-x[1]["alert_count"], x[0]))]

def write_mm_outputs(root:Path, procurement, inventory, vendors, parse_date, svg_bar):
    spend=defaultdict(float)
    for r in procurement: spend[r["category"]]+=float(r["purchase_amount"])
    spend_rows=[{"category":k,"purchase_amount":round(v,2)} for k,v in sorted(spend.items(), key=lambda x:-x[1])]
    vendor_rows=calculate_vendor_performance(procurement,vendors,parse_date); reorder=calculate_reorder_alerts(inventory); risk=calculate_inventory_risk_summary(reorder)
    write_csv(root/"06_MM_Module/outputs/purchase_spend.csv",spend_rows); write_csv(root/"06_MM_Module/outputs/vendor_performance.csv",vendor_rows); write_csv(root/"06_MM_Module/outputs/reorder_alerts.csv",reorder); write_csv(root/"06_MM_Module/outputs/inventory_risk_summary.csv",risk)
    svg_bar(root/"06_MM_Module/outputs/purchase_spend.svg","Purchase Spend by Category",[r["category"] for r in spend_rows],[r["purchase_amount"] for r in spend_rows],"#dc2626")
    worst=max(vendor_rows,key=lambda r:r["vendor_delay_rate_pct"])
    from scripts.analytics_pipeline import write_report
    write_report(root/"06_MM_Module/outputs/mm_report.md","MM Analysis Report",[("Key findings",f"There are {len(reorder)} reorder alerts. Highest vendor delay rate: {worst['vendor_name']} at {worst['vendor_delay_rate_pct']}%."),("Inventory risk summary",md_table(risk)),("Vendor performance",md_table(vendor_rows)),("Reorder alerts",md_table(reorder[:20])),("Management recommendations","Expedite high stock-gap items and review delayed vendors for service-level corrective action or alternate sourcing."),("ERP/SAP relevance","This reflects MM purchasing, goods receipt timing, vendor evaluation, and inventory replenishment monitoring."),("Limitations","No MRP run, safety-stock optimization, batch expiry, or purchase-price variance accounting is modeled.")])
    return {"spend":spend_rows,"vendor_rows":vendor_rows,"reorder":reorder,"risk_summary":risk,"worst_vendor":worst}
