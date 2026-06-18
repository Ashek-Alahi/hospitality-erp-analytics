from __future__ import annotations

import csv
from pathlib import Path


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        rows = [{"message": "No records"}]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def md_table(rows: list[dict[str, object]]) -> str:
    if not rows:
        return "No records."
    headers = list(rows[0].keys())
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join(["---"] * len(headers)) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(header, "")) for header in headers) + " |")
    return "\n".join(lines)


def format_kpi_value(kpi: str, value: object) -> str:
    if isinstance(value, str):
        return value
    if "pct" in kpi.lower() or "rate" in kpi.lower() or "margin" in kpi.lower():
        return f"{float(value):,.2f}%"
    if kpi in {"Total net revenue", "ADR", "RevPAR", "Open AR balance", "Operating profit", "Purchase spend"}:
        return f"${float(value):,.2f}"
    if isinstance(value, int) or float(value).is_integer():
        return f"{float(value):,.0f}"
    return f"{float(value):,.2f}"
