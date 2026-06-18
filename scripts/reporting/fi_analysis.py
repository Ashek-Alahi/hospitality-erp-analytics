from __future__ import annotations

from collections import defaultdict
from datetime import datetime
from pathlib import Path

from scripts.reporting.common import md_table, write_csv

AS_OF_DATE = datetime.strptime("2025-12-31", "%Y-%m-%d")
AS_OF_DATE_TEXT = "2025-12-31"


def parse_date(value: str) -> datetime:
    return datetime.strptime(value, "%Y-%m-%d")


def period(value: str) -> str:
    return value[:7]


def calculate_paid_by_invoice_as_of(payments: list[dict[str, str]]) -> dict[str, float]:
    paid_by_invoice: dict[str, float] = defaultdict(float)
    for payment in payments:
        if parse_date(payment["payment_date"]) <= AS_OF_DATE:
            paid_by_invoice[payment["invoice_id"]] += float(payment["payment_amount"])
    return paid_by_invoice


def calculate_invoice_status(invoices: list[dict[str, str]], payments: list[dict[str, str]]) -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    paid_by_invoice = calculate_paid_by_invoice_as_of(payments)
    detail: list[dict[str, object]] = []
    summary: dict[str, dict[str, object]] = {}
    for invoice in invoices:
        amount = float(invoice["invoice_amount"])
        paid = round(paid_by_invoice.get(invoice["invoice_id"], 0.0), 2)
        outstanding = round(max(amount - paid, 0.0), 2)
        due_date = parse_date(invoice["due_date"])
        if paid >= amount:
            status = "Cleared"
        elif paid > 0:
            status = "Partially Paid"
        elif due_date > AS_OF_DATE:
            status = "Open - Not Yet Due"
        else:
            status = "Open - Overdue"
        detail.append({
            "invoice_id": invoice["invoice_id"],
            "customer_id": invoice["customer_id"],
            "invoice_amount": round(amount, 2),
            "paid_amount_as_of": paid,
            "outstanding_balance_as_of": outstanding,
            "due_date": invoice["due_date"],
            "calculated_status_as_of": status,
        })
        summary.setdefault(status, {"calculated_status_as_of": status, "invoice_count": 0, "invoice_amount": 0.0, "paid_amount_as_of": 0.0, "outstanding_balance_as_of": 0.0})
        summary[status]["invoice_count"] += 1
        summary[status]["invoice_amount"] += round(amount, 2)
        summary[status]["paid_amount_as_of"] += paid
        summary[status]["outstanding_balance_as_of"] += outstanding
    order = ["Cleared", "Partially Paid", "Open - Not Yet Due", "Open - Overdue"]
    rows = []
    for status in order:
        if status in summary:
            row = summary[status]
            rows.append({k: round(v, 2) if isinstance(v, float) else v for k, v in row.items()})
    return detail, rows


def calculate_ar_aging(invoices: list[dict[str, str]], payments: list[dict[str, str]]) -> tuple[list[dict[str, object]], list[dict[str, object]], float]:
    paid_by_invoice = calculate_paid_by_invoice_as_of(payments)
    buckets: dict[str, float] = defaultdict(float)
    overdue_rows: list[dict[str, object]] = []
    for invoice in invoices:
        outstanding = round(float(invoice["invoice_amount"]) - paid_by_invoice.get(invoice["invoice_id"], 0.0), 2)
        days = max(0, (AS_OF_DATE - parse_date(invoice["due_date"])).days)
        bucket = "Current" if days == 0 else "1-30" if days <= 30 else "31-60" if days <= 60 else "61-90" if days <= 90 else "90+"
        if outstanding > 0:
            buckets[bucket] += outstanding
            overdue_rows.append({"invoice_id": invoice["invoice_id"], "customer_id": invoice["customer_id"], "aging_bucket": bucket, "days_past_due": days, "outstanding_balance": outstanding})
    ar_aging = [{"aging_bucket": bucket, "outstanding_balance": round(buckets.get(bucket, 0), 2)} for bucket in ["Current", "1-30", "31-60", "61-90", "90+"]]
    return ar_aging, overdue_rows, round(sum(buckets.values()), 2)


def calculate_collection_rate(invoices: list[dict[str, str]], payments: list[dict[str, str]]) -> tuple[float, float, float]:
    total_invoiced = sum(float(row["invoice_amount"]) for row in invoices if parse_date(row["invoice_date"]) <= AS_OF_DATE)
    total_collected = sum(float(row["payment_amount"]) for row in payments if parse_date(row["payment_date"]) <= AS_OF_DATE)
    return round(total_collected / total_invoiced * 100, 2), round(total_invoiced, 2), round(total_collected, 2)


def calculate_cash_collections(payments: list[dict[str, str]]) -> list[dict[str, object]]:
    grouped: dict[str, float] = defaultdict(float)
    for row in payments:
        if parse_date(row["payment_date"]) <= AS_OF_DATE:
            grouped[period(row["payment_date"])] += float(row["payment_amount"])
    return [{"period": key, "payment_amount": round(value, 2)} for key, value in sorted(grouped.items())]


def write_fi_outputs(root: Path, invoices: list[dict[str, str]], payments: list[dict[str, str]], trend: list[dict[str, object]], svg_bar) -> dict[str, object]:
    ar_aging, overdue_rows, open_ar = calculate_ar_aging(invoices, payments)
    collection_rate, total_invoiced, total_collected = calculate_collection_rate(invoices, payments)
    invoice_detail, invoice_summary = calculate_invoice_status(invoices, payments)
    collections = calculate_cash_collections(payments)
    write_csv(root / "03_FI_Module/outputs/ar_aging.csv", ar_aging)
    write_csv(root / "03_FI_Module/outputs/overdue_receivables_summary.csv", overdue_rows)
    write_csv(root / "03_FI_Module/outputs/revenue_trend.csv", trend)
    write_csv(root / "03_FI_Module/outputs/cash_collections.csv", collections)
    write_csv(root / "03_FI_Module/outputs/invoice_status_detail.csv", invoice_detail)
    write_csv(root / "03_FI_Module/outputs/invoice_status_summary.csv", invoice_summary)
    svg_bar(root / "03_FI_Module/outputs/revenue_trend.svg", "Monthly Net Revenue", [r["period"] for r in trend], [r["net_revenue"] for r in trend])
    report = [
        ("Key findings", f"Collection rate as of {AS_OF_DATE_TEXT} is {collection_rate:.1f}% and open AR is {open_ar:,.2f}."),
        ("As-of-date logic", f"FI receivables and collection KPIs are calculated as of {AS_OF_DATE_TEXT}. Payments after this date are not counted as collected cash for the as-of-date position."),
        ("Invoice status logic", "Statuses are recalculated from invoice amount, payments posted on or before the as-of date, and due date; the generated source status column is not used for reporting."),
        ("Invoice status summary", md_table(invoice_summary)),
        ("AR aging", md_table(ar_aging)),
        ("Business meaning", "Finance should prioritize overdue and partially paid accounts, validate disputed balances, and tighten credit-control follow-up cadence."),
        ("ERP/SAP relevance", "This mirrors FI-AR working-capital monitoring: invoices, clearings, due dates, and dunning priorities are transformed into management KPIs."),
        ("Limitations", "Synthetic data only; no tax, bank statement, lockbox, credit memo, or real customer dispute workflow is modeled."),
    ]
    from scripts.analytics_pipeline import write_report
    write_report(root / "03_FI_Module/outputs/fi_report.md", "FI Analysis Report", report)
    return {"ar_aging": ar_aging, "overdue_rows": overdue_rows, "open_ar": open_ar, "collection_rate": collection_rate, "total_collected_as_of": total_collected, "collections": collections, "invoice_summary": invoice_summary, "invoice_detail": invoice_detail}
