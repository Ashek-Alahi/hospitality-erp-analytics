from pathlib import Path
import csv
import subprocess
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.validate_data import BINARY_EXTENSIONS, REQUIRED_COLUMNS, find_binary_files

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "02_Data" / "processed"

KEY_OUTPUTS = [
    ROOT / "03_FI_Module" / "outputs" / "fi_report.md",
    ROOT / "03_FI_Module" / "outputs" / "ar_aging.csv",
    ROOT / "04_CO_Module" / "outputs" / "co_report.md",
    ROOT / "05_SD_Module" / "outputs" / "sd_report.md",
    ROOT / "06_MM_Module" / "outputs" / "mm_report.md",
    ROOT / "07_Analytics_Forecasting" / "outputs" / "forecast_report.md",
    ROOT / "08_BI_Integration" / "dashboard" / "index.html",
    ROOT / "09_Documentation" / "kpi_summary.csv",
    ROOT / "09_Documentation" / "kpi_summary.md",
]

EXPECTED_KPIS = {
    "Total net revenue",
    "Open AR balance",
    "Operating profit",
    "Purchase spend",
    "Reorder alerts",
}


def read_header(path: Path) -> set[str]:
    with path.open(newline="", encoding="utf-8") as handle:
        return set(next(csv.reader(handle)))


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


def test_pipeline_does_not_generate_binary_files():
    assert not find_binary_files(), "Blocked binary files remain or were generated"
    for path in ROOT.rglob("*"):
        if ".git" in path.parts or "__pycache__" in path.parts or ".pytest_cache" in path.parts:
            continue
        assert path.suffix.lower() not in BINARY_EXTENSIONS
