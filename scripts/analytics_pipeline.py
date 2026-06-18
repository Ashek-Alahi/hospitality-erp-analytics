from __future__ import annotations

import csv
from collections import defaultdict
from datetime import datetime
from pathlib import Path

from scripts.generate_synthetic_data import ROOMS_AVAILABLE, generate_data
from scripts.validate_data import validate_data
from scripts.reporting.common import md_table, write_csv
from scripts.reporting.dashboard import write_dashboard
from scripts.reporting.executive_reports import build_action_register, write_action_register

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "02_Data" / "processed"
AS_OF_DATE = datetime.strptime("2025-12-31", "%Y-%m-%d")


def read_csv(name: str) -> list[dict[str, str]]:
    with (DATA / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def parse_date(value: str) -> datetime:
    return datetime.strptime(value, "%Y-%m-%d")


def period(value: str) -> str:
    return value[:7]


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

    from scripts.reporting.sd_analysis import write_sd_outputs
    from scripts.reporting.fi_analysis import AS_OF_DATE as FI_AS_OF_DATE, write_fi_outputs
    from scripts.reporting.co_analysis import write_co_outputs
    from scripts.reporting.mm_analysis import write_mm_outputs
    from scripts.reporting.forecasting import write_forecast_outputs

    sd = write_sd_outputs(ROOT, sales, customers, svg_bar)
    revenue_by_month = defaultdict(float)
    for row in sales:
        revenue_by_month[period(row["sale_date"])] += float(row["net_revenue"])
    trend = [{"period": key, "net_revenue": round(value, 2)} for key, value in sorted(revenue_by_month.items())]

    fi = write_fi_outputs(ROOT, invoices, payments, trend, svg_bar)
    co = write_co_outputs(ROOT, costs, sd["total_revenue"], svg_bar)
    mm = write_mm_outputs(ROOT, procurement, inventory, vendors, parse_date, svg_bar)
    fc = write_forecast_outputs(ROOT, trend, fi["collections"], payments, parse_date, FI_AS_OF_DATE, svg_bar)

    kpis = [
        {"kpi": "Total net revenue", "value": round(sd["total_revenue"], 2)},
        {"kpi": "Occupancy rate pct", "value": round(sd["occupancy_rate"], 2)},
        {"kpi": "ADR", "value": round(sd["adr"], 2)},
        {"kpi": "RevPAR", "value": round(sd["revpar"], 2)},
        {"kpi": "Collection rate pct as of 2025-12-31", "value": round(fi["collection_rate"], 2)},
        {"kpi": "Open AR balance as of 2025-12-31", "value": round(fi["open_ar"], 2)},
        {"kpi": "Overdue AR exposure", "value": round(sum(float(r["outstanding_balance"]) for r in fi["overdue_rows"] if r["aging_bucket"] != "Current"), 2)},
        {"kpi": "Operating profit", "value": round(co["operating_profit"], 2)},
        {"kpi": "Operating profit margin pct", "value": round(co["margin"], 2)},
        {"kpi": "Purchase spend", "value": round(sum(float(p["purchase_amount"]) for p in procurement), 2)},
        {"kpi": "Vendor delay rate pct", "value": round(sum(1 for v in procurement if parse_date(v["received_date"]) > parse_date(v["promised_date"])) / len(procurement) * 100, 2)},
        {"kpi": "Reorder alerts", "value": len(mm["reorder"])},
        {"kpi": "Items at risk", "value": sum(int(r["items_at_risk"]) for r in mm["risk_summary"])},
        {"kpi": "Max inventory stock gap", "value": max((float(r["max_stock_gap"]) for r in mm["risk_summary"]), default=0)},
        {"kpi": "Best forecast baseline", "value": fc["best"]["model"]},
    ]
    write_csv(ROOT / "09_Documentation/kpi_summary.csv", kpis)
    (ROOT / "09_Documentation/kpi_summary.md").write_text("# KPI Summary\n\n" + md_table(kpis) + "\n", encoding="utf-8")
    actions = build_action_register(kpis, co["cc_rows"], mm["vendor_rows"], mm["reorder"], sd["channel"], fc["best"])
    write_action_register(ROOT, actions)
    write_report(ROOT / "09_Documentation/final_executive_summary.md", "Final Executive Summary", [("Portfolio positioning", "A SAP S/4HANA-inspired hospitality ERP analytics prototype using deterministic synthetic data, Python, SQL-ready CSVs, Markdown reporting, SVG charts, and an HTML dashboard."), ("Most important findings", md_table(kpis)), ("Recommended actions", md_table(actions)), ("Scope note", "This is synthetic-data-based, not a real SAP implementation, and not production-grade forecasting.")])
    write_report(ROOT / "09_Documentation/final_project_report.md", "Final Project Report", [("Business problem", "Hospitality leaders need one management view connecting commercial performance, receivables, cost-center accountability, purchasing reliability, inventory risk, and short-term planning."), ("Project objective", "Build a GitHub-reviewable analytics prototype that converts deterministic synthetic ERP-style CSV data into FI, CO, SD, MM, forecasting, KPI, SQL, and dashboard outputs."), ("Data model summary", "Customer, vendor, and calendar master data connect to sales revenue, invoices, payments, cost-center actuals, procurement records, and inventory movements."), ("FI findings", f"Collection rate is {fi['collection_rate']:.1f}% as of 2025-12-31 with open AR of {fi['open_ar']:,.2f}; payments after the as-of date are excluded from actual cash and invoice status."), ("Invoice status findings", md_table(fi["invoice_summary"])), ("CO findings", f"Operating profit margin is {co['margin']:.1f}%. The largest unfavorable variance is {co['cc_rows'][0]['cost_center_name']} at {co['cc_rows'][0]['variance_pct']:.1f}%."), ("SD findings", f"Occupancy is {sd['occupancy_rate']:.1f}%, ADR is {sd['adr']:,.2f}, and RevPAR is {sd['revpar']:,.2f}."), ("MM findings", f"The prototype identifies {len(mm['reorder'])} reorder alerts using stock-gap risk and vendor delivery variation."), ("Forecasting findings", f"Revenue output separates actual, holdout, and true future forecast rows; {fc['best']['model']} has the best holdout MAPE at {fc['best']['mape_pct']}%."), ("Executive KPI summary", md_table(kpis)), ("Management recommendations", "Prioritize overdue AR follow-up, review unfavorable cost-center variances, refine channel strategy, act on stock gaps, and review delayed vendors."), ("SAP/ERP relevance", "The design is inspired by SAP S/4HANA process areas, master data, transactional documents, exception monitoring, and management reporting while remaining a portfolio analytics prototype."), ("Limitations", "No live SAP connection, no confidential data, no binary BI file, and simplified business logic. Forecasts are directional baselines, not production commitments.")])
    write_dashboard(ROOT, kpis, actions)


if __name__ == "__main__":
    main()
