from pathlib import Path
import csv
import subprocess
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.validate_data import BINARY_EXTENSIONS, REQUIRED_COLUMNS, find_binary_files, validate_data

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "02_Data" / "processed"

KEY_OUTPUTS = [
    ROOT / "03_FI_Module" / "outputs" / "fi_report.md",
    ROOT / "03_FI_Module" / "outputs" / "ar_aging.csv",
    ROOT / "03_FI_Module" / "outputs" / "overdue_receivables_summary.csv",
    ROOT / "03_FI_Module" / "outputs" / "invoice_status_summary.csv",
    ROOT / "04_CO_Module" / "outputs" / "co_report.md",
    ROOT / "04_CO_Module" / "outputs" / "cost_center_variance.csv",
    ROOT / "05_SD_Module" / "outputs" / "sd_report.md",
    ROOT / "05_SD_Module" / "outputs" / "hospitality_kpis.csv",
    ROOT / "06_MM_Module" / "outputs" / "mm_report.md",
    ROOT / "06_MM_Module" / "outputs" / "inventory_risk_summary.csv",
    ROOT / "07_Analytics_Forecasting" / "outputs" / "forecast_report.md",
    ROOT / "07_Analytics_Forecasting" / "outputs" / "cash_collection_forecast.csv",
    ROOT / "08_BI_Integration" / "dashboard" / "index.html",
    ROOT / "09_Documentation" / "kpi_summary.csv",
    ROOT / "09_Documentation" / "kpi_summary.md",
    ROOT / "02_Data" / "sql" / "example_analysis_queries.sql",
    ROOT / "09_Documentation" / "executive_action_register.csv",
    ROOT / "09_Documentation" / "executive_action_register.md",
    ROOT / "01_Project_Foundation" / "ERP_Process_Flows.md",
    ROOT / "09_Documentation" / "kpi_formula_catalog.md",
    ROOT / "09_Documentation" / "interview_handbook.md",
]

EXPECTED_KPIS = {
    "Total net revenue",
    "Occupancy rate pct",
    "ADR",
    "RevPAR",
    "Collection rate pct as of 2025-12-31",
    "Open AR balance as of 2025-12-31",
    "Overdue AR exposure",
    "Operating profit",
    "Operating profit margin pct",
    "Purchase spend",
    "Vendor delay rate pct",
    "Reorder alerts",
    "Best forecast baseline",
}


def read_header(path: Path) -> set[str]:
    with path.open(newline="", encoding="utf-8") as handle:
        return set(next(csv.reader(handle)))


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def test_required_input_csv_files_exist():
    for filename in REQUIRED_COLUMNS:
        assert (DATA / filename).exists(), f"Missing required input file: {filename}"


def test_required_columns_exist():
    for filename, required_columns in REQUIRED_COLUMNS.items():
        assert required_columns <= read_header(DATA / filename)


def test_run_all_executes_successfully():
    result = subprocess.run(
        [sys.executable, "run_all.py"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr


def test_key_output_files_are_generated():
    for path in KEY_OUTPUTS:
        assert path.exists(), f"Missing output: {path.relative_to(ROOT)}"
        assert path.stat().st_size > 0, f"Empty output: {path.relative_to(ROOT)}"


def test_kpi_summary_contains_expected_kpi_names():
    with (ROOT / "09_Documentation" / "kpi_summary.csv").open(newline="", encoding="utf-8") as handle:
        kpis = {row["kpi"] for row in csv.DictReader(handle)}
    assert EXPECTED_KPIS <= kpis


def test_business_exceptions_are_visible():
    aging_buckets = {row["aging_bucket"] for row in read_rows(ROOT / "03_FI_Module" / "outputs" / "ar_aging.csv") if float(row["outstanding_balance"]) > 0}
    assert {"31-60", "61-90", "90+"} <= aging_buckets
    assert read_rows(ROOT / "06_MM_Module" / "outputs" / "reorder_alerts.csv")
    vendors = read_rows(ROOT / "06_MM_Module" / "outputs" / "vendor_performance.csv")
    assert any(float(row["vendor_delay_rate_pct"]) > 0 for row in vendors)
    cost_centers = read_rows(ROOT / "04_CO_Module" / "outputs" / "cost_center_variance.csv")
    assert any(float(row["variance_pct"]) > 0 for row in cost_centers)
    assert any(float(row["variance_pct"]) < 0 for row in cost_centers)


def test_forecast_compares_three_baseline_models():
    metrics = read_rows(ROOT / "07_Analytics_Forecasting" / "outputs" / "forecast_metrics.csv")
    assert {"naive forecast", "moving average forecast", "linear trend forecast"} <= {row["model"] for row in metrics}
    assert {"model", "holdout_months", "mape_pct", "mae"} <= set(metrics[0])


def test_pipeline_does_not_generate_binary_files():
    assert not find_binary_files(), "Blocked binary files remain or were generated"
    for path in ROOT.rglob("*"):
        if ".git" in path.parts or "__pycache__" in path.parts or ".pytest_cache" in path.parts:
            continue
        assert path.suffix.lower() not in BINARY_EXTENSIONS


def test_validation_passes():
    validate_data()


def test_cash_collection_forecast_is_not_mislabeled():
    old_path = ROOT / "07_Analytics_Forecasting" / "outputs" / "cash_flow_forecast.csv"
    new_path = ROOT / "07_Analytics_Forecasting" / "outputs" / "cash_collection_forecast.csv"
    assert not old_path.exists(), "Historical collections must not be mislabeled as cash flow forecast"
    rows = read_rows(new_path)
    assert {"period", "actual_cash_collected", "forecast_cash_collected", "record_type", "method"} <= set(rows[0])
    assert any(row["record_type"] == "actual" for row in rows)
    assert any(row["record_type"] == "forecast" and row["forecast_cash_collected"] for row in rows)


def test_documentation_has_no_draft_cleanup_language():
    blocked_phrases = [
        "former binary image",
        "retained as-is",
        "should attach",
        "future objective",
        "draft-only token",
        "temporary reviewer note",
    ]
    searchable_files = [
        *ROOT.glob("*.md"),
        *ROOT.glob("0*_*/**/*.md"),
        ROOT / "08_BI_Integration" / "dashboard" / "index.html",
    ]
    for path in searchable_files:
        text = path.read_text(encoding="utf-8").lower()
        for phrase in blocked_phrases:
            assert phrase not in text, f"{phrase!r} found in {path.relative_to(ROOT)}"


def test_core_calculation_formulas_are_correct():
    invoices = read_rows(ROOT / "02_Data" / "processed" / "customer_invoices_clean.csv")
    payments = read_rows(ROOT / "02_Data" / "processed" / "customer_payments_clean.csv")
    as_of = "2025-12-31"
    expected_collection_rate = round(sum(float(r["payment_amount"]) for r in payments if r["payment_date"] <= as_of) / sum(float(r["invoice_amount"]) for r in invoices if r["invoice_date"] <= as_of) * 100, 2)
    kpis = {row["kpi"]: row["value"] for row in read_rows(ROOT / "09_Documentation" / "kpi_summary.csv")}
    assert float(kpis["Collection rate pct as of 2025-12-31"]) == expected_collection_rate

    ar_rows = read_rows(ROOT / "03_FI_Module" / "outputs" / "ar_aging.csv")
    assert {"Current", "1-30", "31-60", "61-90", "90+"} == {row["aging_bucket"] for row in ar_rows}

    profitability = {row["metric"]: float(row["amount"]) for row in read_rows(ROOT / "04_CO_Module" / "outputs" / "profitability_summary.csv")}
    assert round(profitability["Operating profit"] / profitability["Net revenue"] * 100, 2) == profitability["Operating profit margin pct"]

    cc = read_rows(ROOT / "04_CO_Module" / "outputs" / "cost_center_variance.csv")[0]
    assert round(float(cc["actual_amount"]) - float(cc["budget_amount"]), 2) == float(cc["variance"])


def test_mm_rules_and_forecast_metric_outputs():
    procurement = read_rows(ROOT / "02_Data" / "processed" / "procurement_vendor_clean.csv")
    expected_delay_rate = round(sum(1 for row in procurement if row["received_date"] > row["promised_date"]) / len(procurement) * 100, 2)
    kpis = {row["kpi"]: row["value"] for row in read_rows(ROOT / "09_Documentation" / "kpi_summary.csv")}
    assert float(kpis["Vendor delay rate pct"]) == expected_delay_rate

    reorder_rows = read_rows(ROOT / "06_MM_Module" / "outputs" / "reorder_alerts.csv")
    assert reorder_rows
    assert all(float(row["closing_stock"]) <= float(row["reorder_point"]) for row in reorder_rows)

    metrics = read_rows(ROOT / "07_Analytics_Forecasting" / "outputs" / "forecast_metrics.csv")
    assert all(row["mape_pct"] and row["mae"] for row in metrics)


def test_as_of_date_invoice_status_and_forecast_outputs():
    as_of = "2025-12-31"
    invoice_status = read_rows(ROOT / "03_FI_Module" / "outputs" / "invoice_status_summary.csv")
    statuses = {row["calculated_status_as_of"] for row in invoice_status}
    assert {"Cleared", "Partially Paid"} <= statuses
    assert any(status.startswith("Open -") for status in statuses)

    inventory_risk = read_rows(ROOT / "06_MM_Module" / "outputs" / "inventory_risk_summary.csv")
    assert {"alert_count", "items_at_risk", "average_stock_gap", "max_stock_gap"} <= set(inventory_risk[0])

    revenue_forecast = read_rows(ROOT / "07_Analytics_Forecasting" / "outputs" / "revenue_forecast.csv")
    assert {"period", "actual_net_revenue", "forecast_net_revenue", "record_type", "method"} <= set(revenue_forecast[0])
    assert {"actual", "holdout", "forecast"} <= {row["record_type"] for row in revenue_forecast}

    cash_rows = read_rows(ROOT / "07_Analytics_Forecasting" / "outputs" / "cash_collection_forecast.csv")
    assert all(row["period"] <= as_of[:7] for row in cash_rows if row["record_type"] == "actual")

    readmes = [ROOT / path for path in ["03_FI_Module/README.md", "04_CO_Module/README.md", "05_SD_Module/README.md", "06_MM_Module/README.md", "07_Analytics_Forecasting/README.md", "08_BI_Integration/README.md"]]
    texts = [path.read_text(encoding="utf-8") for path in readmes]
    assert len(set(texts)) == len(texts)

    catalog = (ROOT / "09_Documentation" / "kpi_formula_catalog.md").read_text(encoding="utf-8")
    for phrase in ["As-of-date collection rate", "Invoice status count", "Inventory stock gap", "Revenue forecast future periods"]:
        assert phrase in catalog
    dashboard = (ROOT / "08_BI_Integration" / "dashboard" / "index.html").read_text(encoding="utf-8")
    assert "Invoice status summary" in dashboard and "Inventory risk summary using stock gap" in dashboard


def test_new_portfolio_documentation_exists_and_is_reviewable():
    required_docs = [
        ROOT / "09_Documentation" / "executive_action_register.csv",
        ROOT / "09_Documentation" / "executive_action_register.md",
        ROOT / "01_Project_Foundation" / "ERP_Process_Flows.md",
        ROOT / "09_Documentation" / "kpi_formula_catalog.md",
        ROOT / "09_Documentation" / "interview_handbook.md",
    ]
    for path in required_docs:
        assert path.exists() and path.stat().st_size > 0
    assert "```mermaid" in (ROOT / "01_Project_Foundation" / "ERP_Process_Flows.md").read_text(encoding="utf-8")
