from __future__ import annotations

import csv
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "02_Data" / "processed"

REQUIRED_COLUMNS = {
    "calendar_clean.csv": {"date", "year", "month", "month_name", "quarter", "day_of_week", "is_weekend"},
    "customers_clean.csv": {"customer_id", "customer_name", "segment", "region"},
    "vendors_clean.csv": {"vendor_id", "vendor_name", "category", "on_time_delivery_pct"},
    "sales_revenue_clean.csv": {"sale_id", "sale_date", "customer_id", "channel", "revenue_category", "net_revenue", "rooms_sold"},
    "customer_invoices_clean.csv": {"invoice_id", "customer_id", "invoice_date", "due_date", "invoice_amount", "status"},
    "customer_payments_clean.csv": {"payment_id", "invoice_id", "payment_date", "payment_amount"},
    "cost_center_budget_actual_clean.csv": {"period", "cost_center_id", "cost_center_name", "budget_amount", "actual_amount"},
    "procurement_vendor_clean.csv": {"po_id", "vendor_id", "order_date", "promised_date", "received_date", "category", "purchase_amount", "quantity"},
    "inventory_movements_clean.csv": {"period", "item_id", "item_name", "category", "opening_stock", "received_qty", "issued_qty", "closing_stock", "reorder_point"},
}

DATE_COLUMNS = {
    "calendar_clean.csv": ["date"],
    "sales_revenue_clean.csv": ["sale_date"],
    "customer_invoices_clean.csv": ["invoice_date", "due_date"],
    "customer_payments_clean.csv": ["payment_date"],
    "procurement_vendor_clean.csv": ["order_date", "promised_date", "received_date"],
}

NON_NEGATIVE_COLUMNS = {
    "sales_revenue_clean.csv": ["net_revenue", "rooms_sold"],
    "customer_invoices_clean.csv": ["invoice_amount"],
    "customer_payments_clean.csv": ["payment_amount"],
    "cost_center_budget_actual_clean.csv": ["budget_amount", "actual_amount"],
    "procurement_vendor_clean.csv": ["purchase_amount", "quantity"],
    "inventory_movements_clean.csv": ["opening_stock", "received_qty", "issued_qty", "closing_stock", "reorder_point"],
}

BINARY_EXTENSIONS = {".png", ".jpg", ".jpeg", ".pdf", ".pbix", ".xlsx", ".db", ".sqlite", ".parquet", ".zip"}


def read_rows(filename: str) -> list[dict[str, str]]:
    path = DATA / filename
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def validate_date(value: str, filename: str, column: str, row_number: int, errors: list[str]) -> None:
    try:
        datetime.strptime(value, "%Y-%m-%d")
    except ValueError:
        errors.append(f"{filename} row {row_number}: {column} must use YYYY-MM-DD format; found {value!r}")


def validate_non_negative(value: str, filename: str, column: str, row_number: int, errors: list[str]) -> None:
    try:
        number = float(value)
    except ValueError:
        errors.append(f"{filename} row {row_number}: {column} must be numeric; found {value!r}")
        return
    if number < 0:
        errors.append(f"{filename} row {row_number}: {column} must be non-negative; found {value!r}")


def find_binary_files(root: Path = ROOT) -> list[Path]:
    ignored_parts = {".git", "__pycache__", ".pytest_cache"}
    return sorted(
        path.relative_to(root)
        for path in root.rglob("*")
        if path.is_file()
        and not any(part in ignored_parts for part in path.parts)
        and path.suffix.lower() in BINARY_EXTENSIONS
    )


def validate_data() -> None:
    errors: list[str] = []
    data: dict[str, list[dict[str, str]]] = {}

    for filename, required_columns in REQUIRED_COLUMNS.items():
        path = DATA / filename
        if not path.exists():
            errors.append(f"Missing required file: {path.relative_to(ROOT)}")
            continue
        rows = read_rows(filename)
        data[filename] = rows
        if not rows:
            errors.append(f"{path.relative_to(ROOT)} must contain at least one data row")
            continue
        actual_columns = set(rows[0].keys())
        missing_columns = sorted(required_columns - actual_columns)
        if missing_columns:
            errors.append(f"{path.relative_to(ROOT)} missing columns: {', '.join(missing_columns)}")
        for row_number, row in enumerate(rows, start=2):
            for column in DATE_COLUMNS.get(filename, []):
                validate_date(row.get(column, ""), filename, column, row_number, errors)
            for column in NON_NEGATIVE_COLUMNS.get(filename, []):
                validate_non_negative(row.get(column, ""), filename, column, row_number, errors)

    customers = {row["customer_id"] for row in data.get("customers_clean.csv", [])}
    vendors = {row["vendor_id"] for row in data.get("vendors_clean.csv", [])}
    invoices = {row["invoice_id"] for row in data.get("customer_invoices_clean.csv", [])}

    for filename in ["sales_revenue_clean.csv", "customer_invoices_clean.csv"]:
        for row_number, row in enumerate(data.get(filename, []), start=2):
            if row.get("customer_id") not in customers:
                errors.append(f"{filename} row {row_number}: unknown customer_id {row.get('customer_id')!r}")
    for row_number, row in enumerate(data.get("customer_payments_clean.csv", []), start=2):
        if row.get("invoice_id") not in invoices:
            errors.append(f"customer_payments_clean.csv row {row_number}: unknown invoice_id {row.get('invoice_id')!r}")
    for row_number, row in enumerate(data.get("procurement_vendor_clean.csv", []), start=2):
        if row.get("vendor_id") not in vendors:
            errors.append(f"procurement_vendor_clean.csv row {row_number}: unknown vendor_id {row.get('vendor_id')!r}")

    binary_files = find_binary_files()
    if binary_files:
        errors.append("Binary files are not allowed: " + ", ".join(str(path) for path in binary_files))

    if errors:
        raise ValueError("Data validation failed:\n- " + "\n- ".join(errors))


if __name__ == "__main__":
    validate_data()
    print("Data validation passed.")
