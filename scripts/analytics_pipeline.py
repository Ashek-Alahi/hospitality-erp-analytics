from __future__ import annotations

import csv
from collections import defaultdict
from datetime import datetime
from pathlib import Path

from scripts.generate_synthetic_data import ROOMS_AVAILABLE, generate_data
from scripts.validate_data import validate_data

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "02_Data" / "processed"
AS_OF_DATE = datetime.strptime("2025-12-31", "%Y-%m-%d")


def read_csv(name: str) -> list[dict[str, str]]:
    with (DATA / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        rows = [{"message": "No records"}]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def parse_date(value: str) -> datetime:
    return datetime.strptime(value, "%Y-%m-%d")


def period(value: str) -> str:
    return value[:7]


def md_table(rows: list[dict[str, object]]) -> str:
    if not rows:
        return "No records."
    headers = list(rows[0].keys())
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join(["---"] * len(headers)) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(header, "")) for header in headers) + " |")
    return "\n".join(lines)


def svg_bar(path: Path, title: str, labels: list[str], values: list[float], color: str = "#2563eb") -> None:
    max_value = max(values) if values else 1
    bar_width = 680 / max(len(values), 1)
    parts = [
        '<svg xmlns="http://www.w3.org/2000/svg" width="960" height="430" viewBox="0 0 960 430">',
        '<rect width="100%" height="100%" fill="white"/>',
        f'<text x="28" y="36" font-family="Arial" font-size="22" font-weight="700">{title}</text>',
    ]
    for index, (label, value) in enumerate(zip(labels, values)):
        height = 290 * value / max_value if max_value else 0
        x = 70 + index * bar_width
        y = 350 - height
        parts += [
            f'<rect x="{x:.1f}" y="{y:.1f}" width="{bar_width * .68:.1f}" height="{height:.1f}" fill="{color}"/>',
            f'<text x="{x:.1f}" y="374" font-family="Arial" font-size="10" transform="rotate(35 {x:.1f},374)">{label}</text>',
            f'<text x="{x:.1f}" y="{y - 6:.1f}" font-family="Arial" font-size="10">{value:,.0f}</text>',
        ]
    parts.append("</svg>")
    path.write_text("\n".join(parts), encoding="utf-8")


def write_report(path: Path, title: str, sections: list[tuple[str, str]]) -> None:
    content = [f"# {title}", "", "Synthetic/anonymized SAP S/4HANA-inspired hospitality ERP analytics prototype. This is not a real SAP implementation.", ""]
    for heading, body in sections:
        content += [f"## {heading}", body, ""]
    path.write_text("\n".join(content), encoding="utf-8")


def group_sum(rows: list[dict[str, str]], key: str, value: str) -> list[dict[str, object]]:
    grouped: dict[str, float] = defaultdict(float)
    for row in rows:
        grouped[row[key]] += float(row[value])
    return [{key: item, value: round(amount, 2)} for item, amount in sorted(grouped.items(), key=lambda x: -x[1])]


def main() -> None:
    generate_data()
    validate_data()
    sales = read_csv("sales_revenue_clean.csv")
    invoices = read_csv("customer_invoices_clean.csv")
    payments = read_csv("customer_payments_clean.csv")
    costs = read_csv("cost_center_budget_actual_clean.csv")
    procurement = read_csv("procurement_vendor_clean.csv")
    inventory = read_csv("inventory_movements_clean.csv")
    customers = {row["customer_id"]: row for row in read_csv("customers_clean.csv")}
    vendors = {row["vendor_id"]: row for row in read_csv("vendors_clean.csv")}

    total_revenue = sum(float(row["net_revenue"]) for row in sales)
    rooms_sold = sum(float(row["rooms_sold"]) for row in sales)
    total_room_revenue = sum(float(row["net_revenue"]) for row in sales if row["revenue_category"] == "Rooms")
    months = sorted({period(row["sale_date"]) for row in sales})
    occupancy_rate = rooms_sold / (ROOMS_AVAILABLE * 30 * len(months)) * 100
    adr = total_room_revenue / rooms_sold
    revpar = total_room_revenue / (ROOMS_AVAILABLE * 30 * len(months))

    paid_by_invoice: dict[str, float] = defaultdict(float)
    for payment in payments:
        paid_by_invoice[payment["invoice_id"]] += float(payment["payment_amount"])
    buckets: dict[str, float] = defaultdict(float)
    overdue_rows = []
    total_invoiced = sum(float(row["invoice_amount"]) for row in invoices)
    total_collected = sum(float(row["payment_amount"]) for row in payments)
    for invoice in invoices:
        outstanding = round(float(invoice["invoice_amount"]) - paid_by_invoice[invoice["invoice_id"]], 2)
        days = max(0, (AS_OF_DATE - parse_date(invoice["due_date"])).days)
        bucket = "Current" if days == 0 else "1-30" if days <= 30 else "31-60" if days <= 60 else "61-90" if days <= 90 else "90+"
        if outstanding > 0:
            buckets[bucket] += outstanding
            overdue_rows.append({"invoice_id": invoice["invoice_id"], "customer_id": invoice["customer_id"], "aging_bucket": bucket, "days_past_due": days, "outstanding_balance": outstanding})
    ar_aging = [{"aging_bucket": bucket, "outstanding_balance": round(buckets.get(bucket, 0), 2)} for bucket in ["Current", "1-30", "31-60", "61-90", "90+"]]
    collection_rate = total_collected / total_invoiced * 100
    revenue_trend = group_sum(sales, "sale_date", "net_revenue")
    revenue_by_month = defaultdict(float)
    for row in sales:
        revenue_by_month[period(row["sale_date"])] += float(row["net_revenue"])
    trend = [{"period": key, "net_revenue": round(value, 2)} for key, value in sorted(revenue_by_month.items())]
    collections_by_month = defaultdict(float)
    for row in payments:
        collections_by_month[period(row["payment_date"])] += float(row["payment_amount"])
    collections = [{"period": key, "payment_amount": round(value, 2)} for key, value in sorted(collections_by_month.items())]
    write_csv(ROOT / "03_FI_Module/outputs/ar_aging.csv", ar_aging)
    write_csv(ROOT / "03_FI_Module/outputs/overdue_receivables_summary.csv", overdue_rows)
    write_csv(ROOT / "03_FI_Module/outputs/revenue_trend.csv", trend)
    write_csv(ROOT / "03_FI_Module/outputs/cash_collections.csv", collections)
    svg_bar(ROOT / "03_FI_Module/outputs/revenue_trend.svg", "Monthly Net Revenue", [r["period"] for r in trend], [r["net_revenue"] for r in trend])
    write_report(ROOT / "03_FI_Module/outputs/fi_report.md", "FI Analysis Report", [("Key findings", f"Collection rate is {collection_rate:.1f}% and open AR is {sum(buckets.values()):,.2f}. The aging profile intentionally includes 31-60, 61-90, and 90+ day exposure for credit-control review."), ("AR aging", md_table(ar_aging)), ("Business meaning", "Finance should prioritize 90+ and 61-90 day accounts, validate disputed balances, and tighten follow-up cadence for group/event and contract receivables."), ("ERP/SAP relevance", "This mirrors FI-AR working-capital monitoring: invoices, clearings, due dates, and dunning priorities are transformed into management KPIs."), ("Limitations", "Synthetic data only; no tax, bank statement, lockbox, credit memo, or real customer dispute workflow is modeled.")])

    cc = defaultdict(lambda: [0.0, 0.0, ""])
    for row in costs:
        cc[row["cost_center_id"]][0] += float(row["budget_amount"])
        cc[row["cost_center_id"]][1] += float(row["actual_amount"])
        cc[row["cost_center_id"]][2] = row["cost_center_name"]
    cc_rows = []
    for cc_id, values in cc.items():
        variance = values[1] - values[0]
        cc_rows.append({"cost_center_id": cc_id, "cost_center_name": values[2], "budget_amount": round(values[0], 2), "actual_amount": round(values[1], 2), "variance": round(variance, 2), "variance_pct": round(variance / values[0] * 100, 2)})
    cc_rows.sort(key=lambda row: row["variance"], reverse=True)
    total_cost = sum(float(row["actual_amount"]) for row in costs)
    operating_profit = total_revenue - total_cost
    margin = operating_profit / total_revenue * 100
    profitability = [{"metric": "Net revenue", "amount": round(total_revenue, 2)}, {"metric": "Operating cost", "amount": round(total_cost, 2)}, {"metric": "Operating profit", "amount": round(operating_profit, 2)}, {"metric": "Operating profit margin pct", "amount": round(margin, 2)}]
    write_csv(ROOT / "04_CO_Module/outputs/cost_center_variance.csv", cc_rows)
    write_csv(ROOT / "04_CO_Module/outputs/profitability_summary.csv", profitability)
    svg_bar(ROOT / "04_CO_Module/outputs/cost_center_actuals.svg", "Actual Cost by Cost Center", [r["cost_center_name"] for r in cc_rows], [r["actual_amount"] for r in cc_rows], "#7c3aed")
    write_report(ROOT / "04_CO_Module/outputs/co_report.md", "CO Analysis Report", [("Key findings", f"Operating profit margin is {margin:.1f}%. Highest unfavorable variance: {cc_rows[0]['cost_center_name']} at {cc_rows[0]['variance_pct']:.1f}%."), ("Budget variance ranking", md_table(cc_rows)), ("Management recommendations", "Review departments with positive variance first, especially operational areas affected by seasonality. Preserve under-budget controls only after confirming service quality was not reduced."), ("ERP/SAP relevance", "The analysis resembles CO cost center planning versus actual postings and profitability review."), ("Limitations", "No allocation cycles, internal orders, activity types, or product/customer profitability ledgers are modeled.")])

    category = group_sum(sales, "revenue_category", "net_revenue")
    channel = group_sum(sales, "channel", "net_revenue")
    segment_values = defaultdict(float)
    for row in sales:
        segment_values[customers[row["customer_id"]]["segment"]] += float(row["net_revenue"])
    segments = [{"segment": key, "net_revenue": round(value, 2)} for key, value in sorted(segment_values.items(), key=lambda x: -x[1])]
    hospitality = [{"kpi": "Occupancy rate pct", "value": round(occupancy_rate, 2)}, {"kpi": "ADR", "value": round(adr, 2)}, {"kpi": "RevPAR", "value": round(revpar, 2)}]
    write_csv(ROOT / "05_SD_Module/outputs/revenue_by_category.csv", category)
    write_csv(ROOT / "05_SD_Module/outputs/revenue_by_channel.csv", channel)
    write_csv(ROOT / "05_SD_Module/outputs/customer_segment_revenue.csv", segments)
    write_csv(ROOT / "05_SD_Module/outputs/hospitality_kpis.csv", hospitality)
    svg_bar(ROOT / "05_SD_Module/outputs/revenue_by_channel.svg", "Revenue by Sales Channel", [r["channel"] for r in channel], [r["net_revenue"] for r in channel], "#059669")
    write_report(ROOT / "05_SD_Module/outputs/sd_report.md", "SD Analysis Report", [("Key findings", f"Occupancy is {occupancy_rate:.1f}%, ADR is {adr:,.2f}, and RevPAR is {revpar:,.2f}."), ("Hospitality KPIs", md_table(hospitality)), ("Revenue by channel", md_table(channel)), ("Revenue by segment", md_table(segments)), ("Business meaning", "Channel and segment mix should guide pricing, promotion timing, and direct-booking strategy. OTA volume should be balanced against margin and commission pressure."), ("ERP/SAP relevance", "This is SD-inspired order/billing analytics connected to customer master segments and revenue categories."), ("Limitations", "No reservations system integration, cancellations, commissions, loyalty tiering, or daily room type inventory is included.")])

    spend = group_sum(procurement, "category", "purchase_amount")
    vendor_stats = defaultdict(lambda: [0.0, 0, 0, 0, ""])
    for row in procurement:
        delay = max(0, (parse_date(row["received_date"]) - parse_date(row["promised_date"])).days)
        stat = vendor_stats[row["vendor_id"]]
        stat[0] += float(row["purchase_amount"]); stat[1] += delay; stat[2] += 1; stat[3] += 1 if delay > 0 else 0; stat[4] = vendors[row["vendor_id"]]["vendor_name"]
    vendor_rows = [{"vendor_id": key, "vendor_name": v[4], "purchase_amount": round(v[0], 2), "avg_delivery_delay_days": round(v[1] / v[2], 2), "vendor_delay_rate_pct": round(v[3] / v[2] * 100, 2), "on_time_delivery_pct": round((v[2] - v[3]) / v[2] * 100, 2)} for key, v in sorted(vendor_stats.items())]
    reorder = [{key: row[key] for key in ["period", "item_id", "item_name", "category", "closing_stock", "reorder_point"]} for row in inventory if float(row["closing_stock"]) <= float(row["reorder_point"])]
    risk_summary = group_sum(reorder, "category", "closing_stock") if reorder else []
    write_csv(ROOT / "06_MM_Module/outputs/purchase_spend.csv", spend)
    write_csv(ROOT / "06_MM_Module/outputs/vendor_performance.csv", vendor_rows)
    write_csv(ROOT / "06_MM_Module/outputs/reorder_alerts.csv", reorder)
    write_csv(ROOT / "06_MM_Module/outputs/inventory_risk_summary.csv", risk_summary)
    svg_bar(ROOT / "06_MM_Module/outputs/purchase_spend.svg", "Purchase Spend by Category", [r["category"] for r in spend], [r["purchase_amount"] for r in spend], "#dc2626")
    worst_vendor = max(vendor_rows, key=lambda r: r["vendor_delay_rate_pct"])
    write_report(ROOT / "06_MM_Module/outputs/mm_report.md", "MM Analysis Report", [("Key findings", f"There are {len(reorder)} reorder alerts. Highest vendor delay rate: {worst_vendor['vendor_name']} at {worst_vendor['vendor_delay_rate_pct']}%."), ("Vendor performance", md_table(vendor_rows)), ("Reorder alerts", md_table(reorder[:20])), ("Management recommendations", "Expedite high-risk items below reorder point and review delayed vendors for service-level corrective action or alternate sourcing."), ("ERP/SAP relevance", "This reflects MM purchasing, goods receipt timing, vendor evaluation, and inventory replenishment monitoring."), ("Limitations", "No MRP run, safety-stock optimization, batch expiry, or purchase-price variance accounting is modeled.")])

    actuals = [float(row["net_revenue"]) for row in trend]
    forecast_rows = []
    metrics = []
    train_end = len(actuals) - 3
    models = {}
    models["naive forecast"] = [actuals[i - 1] if i else actuals[0] for i in range(len(actuals))]
    models["moving average forecast"] = [sum(actuals[max(0, i - 3):i] or [actuals[0]]) / len(actuals[max(0, i - 3):i] or [actuals[0]]) for i in range(len(actuals))]
    slope = (actuals[train_end - 1] - actuals[0]) / max(train_end - 1, 1)
    models["linear trend forecast"] = [actuals[0] + slope * i for i in range(len(actuals))]
    for name, predictions in models.items():
        errors = [abs(actuals[i] - predictions[i]) for i in range(train_end, len(actuals))]
        mape = sum(errors[j] / actuals[train_end + j] for j in range(len(errors))) / len(errors) * 100
        metrics.append({"model": name, "holdout_months": 3, "mape_pct": round(mape, 2), "mae": round(sum(errors) / len(errors), 2)})
    best = min(metrics, key=lambda row: row["mape_pct"])
    for i, row in enumerate(trend):
        forecast_rows.append({"period": row["period"], "net_revenue": row["net_revenue"], "naive_forecast": round(models["naive forecast"][i], 2), "moving_average_forecast": round(models["moving average forecast"][i], 2), "linear_trend_forecast": round(models["linear trend forecast"][i], 2), "recommended_baseline": best["model"]})
    write_csv(ROOT / "07_Analytics_Forecasting/outputs/revenue_forecast.csv", forecast_rows)
    write_csv(ROOT / "07_Analytics_Forecasting/outputs/forecast_metrics.csv", metrics)
    write_csv(ROOT / "07_Analytics_Forecasting/outputs/cash_flow_forecast.csv", collections)
    svg_bar(ROOT / "07_Analytics_Forecasting/outputs/revenue_forecast.svg", "Recommended Revenue Forecast Baseline", [r["period"] for r in forecast_rows], [r[best["model"].replace(" forecast", "_forecast").replace(" ", "_")] for r in forecast_rows], "#ea580c")
    write_report(ROOT / "07_Analytics_Forecasting/outputs/forecast_report.md", "Analytics and Forecasting Report", [("Key findings", f"Compared naive, moving average, and linear trend baselines. Best holdout MAPE is {best['mape_pct']}% from {best['model']}."), ("Forecast metrics", md_table(metrics)), ("Business meaning", "Use the selected baseline as a planning reference only, not an automated commitment. Large variances should trigger review of events, pricing, channel mix, and seasonality."), ("ERP/SAP relevance", "Forecast outputs can support demand planning, cash planning, and management reporting outside core transactional processing."), ("Limitations", "This is not production-grade forecasting; it excludes holidays, events, competitor rates, weather, and formal backtesting across many seasons.")])

    kpis = [
        {"kpi": "Total net revenue", "value": round(total_revenue, 2)}, {"kpi": "Occupancy rate pct", "value": round(occupancy_rate, 2)}, {"kpi": "ADR", "value": round(adr, 2)}, {"kpi": "RevPAR", "value": round(revpar, 2)}, {"kpi": "Collection rate pct", "value": round(collection_rate, 2)}, {"kpi": "Open AR balance", "value": round(sum(buckets.values()), 2)}, {"kpi": "Operating profit", "value": round(operating_profit, 2)}, {"kpi": "Operating profit margin pct", "value": round(margin, 2)}, {"kpi": "Purchase spend", "value": round(sum(float(p["purchase_amount"]) for p in procurement), 2)}, {"kpi": "Vendor delay rate pct", "value": round(sum(1 for v in procurement if parse_date(v["received_date"]) > parse_date(v["promised_date"])) / len(procurement) * 100, 2)}, {"kpi": "Reorder alerts", "value": len(reorder)}, {"kpi": "Best forecast baseline", "value": best["model"]},
    ]
    write_csv(ROOT / "09_Documentation/kpi_summary.csv", kpis)
    (ROOT / "09_Documentation/kpi_summary.md").write_text("# KPI Summary\n\n" + md_table(kpis) + "\n", encoding="utf-8")
    write_report(ROOT / "09_Documentation/final_executive_summary.md", "Final Executive Summary", [("Portfolio positioning", "A SAP S/4HANA-inspired hospitality ERP analytics prototype using deterministic synthetic data, Python, SQL-ready CSVs, Markdown reporting, SVG charts, and an HTML dashboard."), ("Most important findings", md_table(kpis)), ("Recommended actions", "Prioritize overdue AR follow-up, review unfavorable cost centers, protect high-performing direct and contract revenue channels, and mitigate vendor/inventory risks before service levels are affected."), ("Limitations", "Synthetic/anonymized data only; not a real SAP S/4HANA implementation and not production forecasting.")])
    write_report(ROOT / "09_Documentation/final_project_report.md", "Final Project Report", [("Business problem", "Hospitality management needs connected visibility across revenue, receivables, cost control, procurement, inventory, and forecast planning."), ("ERP module coverage", "FI covers AR aging and collections; CO covers budget variance and operating margin; SD covers occupancy, ADR, RevPAR, channel, segment, and category revenue; MM covers vendor delays and reorder risk."), ("KPI summary", md_table(kpis)), ("Management recommendations", "Use the reports as an exception dashboard: collect aged receivables, investigate cost-center overruns, refine pricing/channel strategy, and act on vendor or reorder alerts."), ("SAP relevance", "The design is inspired by SAP S/4HANA process areas, master data, documents, and management reporting, but it is a portfolio prototype only."), ("Limitations", "No live SAP connection, no confidential data, no binary BI file, and simplified business logic.")])

    cards = "".join(f"<div class='card'><span>{row['kpi']}</span><strong>{row['value']}</strong></div>" for row in kpis)
    links = "".join(f"<li><a href='{href}'>{label}</a></li>" for label, href in [("FI report", "../../03_FI_Module/outputs/fi_report.md"), ("CO report", "../../04_CO_Module/outputs/co_report.md"), ("SD report", "../../05_SD_Module/outputs/sd_report.md"), ("MM report", "../../06_MM_Module/outputs/mm_report.md"), ("Forecast report", "../../07_Analytics_Forecasting/outputs/forecast_report.md"), ("Final report", "../../09_Documentation/final_project_report.md")])
    html = f"""<!doctype html><html><head><meta charset='utf-8'><title>Hospitality ERP Analytics Dashboard</title><style>body{{font-family:Arial;margin:28px;color:#111827;background:#f8fafc}}.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(190px,1fr));gap:14px}}.card{{background:white;border:1px solid #d1d5db;border-radius:10px;padding:15px}}.card span{{display:block;color:#4b5563;font-size:13px}}.card strong{{font-size:23px}}iframe{{width:100%;height:430px;border:1px solid #e5e7eb;background:white;border-radius:10px;margin:10px 0}}a{{color:#2563eb}}</style></head><body><h1>Hospitality ERP Analytics Dashboard</h1><p>SAP S/4HANA-inspired prototype using deterministic synthetic/anonymized data only. Charts are SVG/text-based; no screenshots or binary BI files are generated.</p><section class='grid'>{cards}</section><h2>Module charts</h2><iframe src='../../03_FI_Module/outputs/revenue_trend.svg'></iframe><iframe src='../../04_CO_Module/outputs/cost_center_actuals.svg'></iframe><iframe src='../../05_SD_Module/outputs/revenue_by_channel.svg'></iframe><iframe src='../../06_MM_Module/outputs/purchase_spend.svg'></iframe><iframe src='../../07_Analytics_Forecasting/outputs/revenue_forecast.svg'></iframe><h2>Reports</h2><ul>{links}</ul></body></html>"""
    (ROOT / "08_BI_Integration/dashboard/index.html").write_text(html, encoding="utf-8")


if __name__ == "__main__":
    main()
