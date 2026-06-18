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
]

EXPECTED_KPIS = {
    "Total net revenue",
    "Occupancy rate pct",
    "ADR",
    "RevPAR",
    "Collection rate pct",
    "Open AR balance",
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


def test_documentation_has_no_unfinished_cleanup_language():
    blocked_phrases = [
        "former binary image",
        "retained as-is",
        "should attach",
        "future objective",
        "placeholder",
        "manual note",
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
