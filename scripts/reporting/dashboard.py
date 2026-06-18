from __future__ import annotations

import csv
from pathlib import Path
from scripts.reporting.common import format_kpi_value

GROUPS = {
    "FI": {"Total net revenue", "Collection rate pct as of 2025-12-31", "Open AR balance as of 2025-12-31", "Overdue AR exposure"},
    "CO": {"Operating profit", "Operating profit margin pct"},
    "SD": {"Occupancy rate pct", "ADR", "RevPAR"},
    "MM": {"Purchase spend", "Vendor delay rate pct", "Reorder alerts", "Items at risk", "Max inventory stock gap"},
    "Forecasting": {"Best forecast baseline"},
}


def _read_csv(path: Path, limit: int = 8) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))[:limit]


def _html_table(rows: list[dict[str, object]]) -> str:
    if not rows:
        return "<p>No records.</p>"
    headers = list(rows[0].keys())
    head = "".join(f"<th>{h}</th>" for h in headers)
    body = "".join("<tr>" + "".join(f"<td>{r.get(h, '')}</td>" for h in headers) + "</tr>" for r in rows)
    return f"<table><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table>"


def _card_group(kpis: list[dict[str, object]], group: str) -> str:
    cards = "".join(f"<div class='card'><span>{row['kpi']}</span><strong>{format_kpi_value(row['kpi'], row['value'])}</strong></div>" for row in kpis if row["kpi"] in GROUPS[group])
    return f"<section><h2>{group} KPIs</h2><p>{_group_note(group)}</p><div class='grid'>{cards}</div></section>"


def _group_note(group: str) -> str:
    return {"FI": "As-of-date FI KPIs exclude payments after 2025-12-31 from collected cash and open AR.", "CO": "Controlling indicators connect revenue performance to departmental cost accountability.", "SD": "Commercial KPIs show hotel demand, pricing, room productivity, channels, and segments.", "MM": "Procurement and inventory KPIs highlight supplier reliability and stock-gap risk.", "Forecasting": "Baseline forecasts separate actual, holdout, and future forecast rows; they are not production-grade predictions."}[group]


def write_dashboard(root: Path, kpis: list[dict[str, object]], actions: list[dict[str, object]]) -> None:
    grouped_cards = "\n".join(_card_group(kpis, group) for group in GROUPS)
    action_rows = "".join(f"<tr><td>{a['action_id']}</td><td>{a['module']}</td><td>{a['issue']}</td><td>{a['priority']}</td><td>{a['recommended_action']}</td></tr>" for a in actions)
    links = "".join(f"<li><a href='{href}'>{label}</a></li>" for label, href in [("FI report", "../../03_FI_Module/outputs/fi_report.md"), ("CO report", "../../04_CO_Module/outputs/co_report.md"), ("SD report", "../../05_SD_Module/outputs/sd_report.md"), ("MM report", "../../06_MM_Module/outputs/mm_report.md"), ("Forecast report", "../../07_Analytics_Forecasting/outputs/forecast_report.md"), ("Executive action register", "../../09_Documentation/executive_action_register.md"), ("Final report", "../../09_Documentation/final_project_report.md")])
    invoice_status = _html_table(_read_csv(root / "03_FI_Module/outputs/invoice_status_summary.csv"))
    inventory_risk = _html_table(_read_csv(root / "06_MM_Module/outputs/inventory_risk_summary.csv"))
    revenue_future = _html_table([r for r in _read_csv(root / "07_Analytics_Forecasting/outputs/revenue_forecast.csv", 200) if r.get("record_type") == "forecast"][:9])
    cash_future = _html_table([r for r in _read_csv(root / "07_Analytics_Forecasting/outputs/cash_collection_forecast.csv", 200) if r.get("record_type") in {"forecast", "future_scheduled_payment"}][:9])
    html = f"""<!doctype html><html><head><meta charset='utf-8'><title>Hospitality ERP Analytics Dashboard</title><style>
body {{ font-family: Arial, sans-serif; margin: 28px; color: #111827; background: #f8fafc; line-height: 1.45; }}
.grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(190px, 1fr)); gap: 14px; }}
.card, .panel {{ background: white; border: 1px solid #d1d5db; border-radius: 10px; padding: 15px; margin-bottom: 18px; }}
.card span {{ display: block; color: #4b5563; font-size: 13px; }} .card strong {{ font-size: 23px; }} iframe {{ width: 100%; height: 430px; border: 1px solid #e5e7eb; background: white; border-radius: 10px; margin: 10px 0; }}
a {{ color: #2563eb; }} table {{ border-collapse: collapse; width: 100%; background: white; margin-bottom:18px; }} th, td {{ border: 1px solid #d1d5db; padding: 8px; text-align: left; }} th {{ background: #e5e7eb; }} .note {{ background: #fff7ed; border-left: 5px solid #f97316; padding: 12px; }}
</style></head><body>
<h1>Hospitality ERP Analytics Dashboard</h1>
<div class='note'><strong>Scope note:</strong> SAP S/4HANA-inspired prototype using deterministic synthetic data only. This is not a real SAP implementation, does not connect to a live ERP system, and does not use confidential company data. <strong>As-of date:</strong> 2025-12-31.</div>
<section class='panel'><h2>Executive summary</h2><p>This static dashboard connects FI, CO, SD, MM, and forecasting outputs for review of revenue, cash collection, cost accountability, procurement reliability, inventory stock gaps, and planning signals.</p></section>
{grouped_cards}
<section><h2>Invoice status summary as of 2025-12-31</h2>{invoice_status}</section>
<section><h2>Inventory risk summary using stock gap</h2>{inventory_risk}</section>
<section><h2>Revenue forecast future periods</h2>{revenue_future}</section>
<section><h2>Cash collection forecast and scheduled future payments</h2>{cash_future}</section>
<section><h2>Executive action register</h2><table><thead><tr><th>ID</th><th>Module</th><th>Issue</th><th>Priority</th><th>Recommended action</th></tr></thead><tbody>{action_rows}</tbody></table></section>
<h2>Module charts</h2><iframe src='../../03_FI_Module/outputs/revenue_trend.svg'></iframe><iframe src='../../04_CO_Module/outputs/cost_center_actuals.svg'></iframe><iframe src='../../05_SD_Module/outputs/revenue_by_channel.svg'></iframe><iframe src='../../06_MM_Module/outputs/purchase_spend.svg'></iframe><iframe src='../../07_Analytics_Forecasting/outputs/revenue_forecast.svg'></iframe>
<h2>Reports and review links</h2><ul>{links}</ul></body></html>"""
    (root / "08_BI_Integration/dashboard/index.html").write_text(html, encoding="utf-8")
