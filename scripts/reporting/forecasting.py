from __future__ import annotations
from datetime import datetime
from pathlib import Path
from scripts.reporting.common import md_table, write_csv


def add_month(period_text, h):
    d=datetime.strptime(period_text+"-01","%Y-%m-%d"); y=d.year+(d.month+h-1)//12; m=(d.month+h-1)%12+1; return f"{y}-{m:02d}"

def _models(actuals):
    n=len(actuals); train_end=n-3; slope=(actuals[train_end-1]-actuals[0])/max(train_end-1,1)
    return {
        "naive forecast":[actuals[i-1] if i else actuals[0] for i in range(n)],
        "moving average forecast":[sum(actuals[max(0,i-3):i] or [actuals[0]])/len(actuals[max(0,i-3):i] or [actuals[0]]) for i in range(n)],
        "linear trend forecast":[actuals[0]+slope*i for i in range(n)],
    }

def calculate_revenue_forecasts(trend):
    actuals=[float(r["net_revenue"]) for r in trend]; periods=[r["period"] for r in trend]; train_end=len(actuals)-3; models=_models(actuals); metrics=[]
    for name,preds in models.items():
        errors=[abs(actuals[i]-preds[i]) for i in range(train_end,len(actuals))]
        mape=sum(errors[j]/actuals[train_end+j] for j in range(len(errors)))/len(errors)*100
        metrics.append({"model":name,"holdout_months":3,"mape_pct":round(mape,2),"mae":round(sum(errors)/len(errors),2)})
    rows=[]
    for name,preds in models.items():
        for i,p in enumerate(periods):
            rows.append({"period":p,"actual_net_revenue":round(actuals[i],2),"forecast_net_revenue":"" if i<train_end else round(preds[i],2),"record_type":"actual" if i<train_end else "holdout","method":name})
    # future for each method
    for name in models:
        rolling=actuals[:]
        if name=="linear trend forecast": slope=(actuals[train_end-1]-actuals[0])/max(train_end-1,1)
        for h in range(1,4):
            if name=="naive forecast": fv=rolling[-1]
            elif name=="moving average forecast": fv=sum(rolling[-3:])/3
            else: fv=actuals[0]+slope*(len(actuals)+h-1)
            rolling.append(fv)
            rows.append({"period":add_month(periods[-1],h),"actual_net_revenue":"","forecast_net_revenue":round(fv,2),"record_type":"forecast","method":name})
    best=min(metrics,key=lambda r:r["mape_pct"])
    return rows, metrics, best

def calculate_cash_collection_forecast(collections, payments=None, parse_date=None, as_of_date=None):
    rows=[]
    for r in collections: rows.append({"period":r["period"],"actual_cash_collected":r["payment_amount"],"forecast_cash_collected":"","record_type":"actual","method":"historical collections as of date"})
    last=collections[-1]["period"]; rolling=[float(r["payment_amount"]) for r in collections]
    for h in range(1,4):
        fv=round(sum(rolling[-3:])/min(len(rolling),3),2); rolling.append(fv)
        rows.append({"period":add_month(last,h),"actual_cash_collected":"","forecast_cash_collected":fv,"record_type":"forecast","method":"three-month moving average"})
    if payments and parse_date and as_of_date:
        future={}
        for p in payments:
            if parse_date(p["payment_date"])>as_of_date:
                future[p["payment_date"][:7]]=future.get(p["payment_date"][:7],0)+float(p["payment_amount"])
        for p,v in sorted(future.items()):
            rows.append({"period":p,"actual_cash_collected":"","forecast_cash_collected":round(v,2),"record_type":"future_scheduled_payment","method":"known future-dated synthetic payment, excluded from actuals"})
    return rows

def calculate_forecast_metrics(metrics): return metrics

def write_forecast_outputs(root:Path, trend, collections, payments, parse_date, as_of_date, svg_bar):
    rev, metrics, best=calculate_revenue_forecasts(trend); cash=calculate_cash_collection_forecast(collections,payments,parse_date,as_of_date)
    write_csv(root/"07_Analytics_Forecasting/outputs/revenue_forecast.csv",rev); write_csv(root/"07_Analytics_Forecasting/outputs/forecast_metrics.csv",metrics); write_csv(root/"07_Analytics_Forecasting/outputs/cash_collection_forecast.csv",cash)
    legacy=root/"07_Analytics_Forecasting/outputs/cash_flow_forecast.csv"
    if legacy.exists(): legacy.unlink()
    chart=[r for r in rev if r["method"]==best["model"] and r["record_type"] in {"holdout","forecast"}]
    svg_bar(root/"07_Analytics_Forecasting/outputs/revenue_forecast.svg","Revenue Baseline Holdout and Future Forecast",[r["period"] for r in chart],[float(r["forecast_net_revenue"]) for r in chart],"#ea580c")
    from scripts.analytics_pipeline import write_report
    write_report(root/"07_Analytics_Forecasting/outputs/forecast_report.md","Analytics and Forecasting Report",[("Key findings",f"Compared naive, moving average, and linear trend baselines. Best holdout MAPE is {best['mape_pct']}% from {best['model']}. Future periods begin after the latest actual revenue month."),("Revenue forecast record types","`actual` rows are training history, `holdout` rows compare baseline predictions against known actuals, and `forecast` rows are true future periods."),("Revenue forecast metrics",md_table(metrics)),("Cash collection forecast",md_table(cash[-8:])),("Business meaning","Use these baselines as directional planning references only; future-dated payments are labeled separately and not mixed with historical actuals."),("ERP/SAP relevance","Forecast outputs support demand planning, cash collection planning, and management reporting outside core transactional processing."),("Limitations","This is not production-grade forecasting; it excludes events, competitor rates, weather, disputes, and formal multi-season backtesting.")])
    return {"revenue_forecast":rev,"forecast_metrics":metrics,"cash_forecast":cash,"best":best}
