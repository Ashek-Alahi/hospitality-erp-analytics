from __future__ import annotations

from pathlib import Path

from scripts.reporting.common import md_table, write_csv


def build_action_register(kpis: list[dict[str, object]], cc_rows: list[dict[str, object]], vendor_rows: list[dict[str, object]], reorder: list[dict[str, object]], channel_rows: list[dict[str, object]], forecast_best: dict[str, object]) -> list[dict[str, object]]:
    kpi_lookup = {row["kpi"]: row["value"] for row in kpis}
    worst_cc = cc_rows[0]
    worst_vendor = max(vendor_rows, key=lambda row: float(row["vendor_delay_rate_pct"]))
    top_channel = channel_rows[0]
    return [
        {"action_id": "ACT-001", "module": "FI", "issue": "Overdue receivables as of date", "evidence": f"Open AR balance {float(kpi_lookup.get('Open AR balance as of 2025-12-31', kpi_lookup.get('Open AR balance', 0))):,.2f}", "priority": "High", "recommended_action": "Prioritize overdue and partially paid receivables using as-of-date invoice status and aging.", "owner_role": "Finance / Credit Control", "expected_business_value": "Improve cash conversion and reduce write-off exposure."},
        {"action_id": "ACT-002", "module": "MM", "issue": "High vendor delay rate", "evidence": f"{worst_vendor['vendor_name']} delay rate {worst_vendor['vendor_delay_rate_pct']}%", "priority": "High", "recommended_action": "Review service levels, expedite open items, and identify alternate suppliers for critical categories.", "owner_role": "Procurement Manager", "expected_business_value": "Protect guest service levels and reduce emergency purchasing."},
        {"action_id": "ACT-003", "module": "MM", "issue": "Inventory stock gap risk", "evidence": f"{len(reorder)} reorder alerts generated", "priority": "High", "recommended_action": "Replenish high stock-gap items and confirm reorder points for seasonal demand.", "owner_role": "Inventory Controller", "expected_business_value": "Reduce stockout risk in housekeeping, F&B, and maintenance operations."},
        {"action_id": "ACT-004", "module": "CO", "issue": "Unfavorable cost center variance", "evidence": f"{worst_cc['cost_center_name']} variance {worst_cc['variance_pct']}%", "priority": "Medium", "recommended_action": "Review spending drivers and update department action plans.", "owner_role": "Department Manager / Controller", "expected_business_value": "Improve budget accountability without reducing service quality."},
        {"action_id": "ACT-005", "module": "SD", "issue": "Revenue concentration by channel", "evidence": f"Top channel is {top_channel['channel']} at {float(top_channel['net_revenue']):,.2f}", "priority": "Medium", "recommended_action": "Review direct booking, negotiated account, and OTA channel mix.", "owner_role": "Revenue Manager", "expected_business_value": "Reduce margin pressure and strengthen commercial resilience."},
        {"action_id": "ACT-006", "module": "Forecasting", "issue": "Weak forecast reliability", "evidence": f"Best baseline {forecast_best['model']} MAPE {forecast_best['mape_pct']}%", "priority": "Medium", "recommended_action": "Use baseline forecasts as planning signals and investigate large variances before commitments.", "owner_role": "FP&A / Revenue Management", "expected_business_value": "Improve short-term planning discipline while avoiding overconfidence."},
    ]


def write_action_register(root: Path, actions: list[dict[str, object]]) -> None:
    csv_path = root / "09_Documentation" / "executive_action_register.csv"
    md_path = root / "09_Documentation" / "executive_action_register.md"
    write_csv(csv_path, actions)
    md_path.write_text("# Executive Action Register\n\n" + md_table(actions) + "\n", encoding="utf-8")
