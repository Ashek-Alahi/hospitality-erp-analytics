# Hospitality ERP Analytics Portfolio Project

A professional **SAP S/4HANA-inspired hospitality ERP analytics prototype** built with deterministic synthetic/anonymized data only. This repository does **not** claim to be a real SAP S/4HANA implementation. It demonstrates how ERP-style FI, CO, SD, MM, forecasting, SQL, Python automation, and BI-style reporting can be organized in a GitHub-reviewable analytics project.

## Business Problem

Hotel leadership often reviews revenue, receivables, operating cost control, procurement reliability, inventory risk, and short-term planning in separate reports. This project connects those topics into a small ERP-style analytics workflow so business users can review exceptions, KPIs, and management actions together.

## What This Project Demonstrates

- ERP analytics across FI, CO, SD, and MM process areas.
- Accounting logic for AR aging, collections, profitability, and cost-center variance.
- KPI design for hospitality and management reporting, including occupancy, ADR, RevPAR, collection rate, open AR, operating margin, vendor delay rate, and reorder alerts.
- SQL-ready table structures and example analysis queries.
- Python automation for deterministic data generation, validation, reporting, charts, and dashboard output.
- Business decision-making through concise findings, limitations, and management recommendations.

## ERP Module Coverage

| Module | Analytics coverage | Important outputs |
| --- | --- | --- |
| FI | AR aging, overdue receivables, collection rate, revenue trend, cash collections | `03_FI_Module/outputs/fi_report.md` |
| CO | Budget vs actual, variance percentage, unfavorable cost-center ranking, operating profit margin | `04_CO_Module/outputs/co_report.md` |
| SD | Occupancy, ADR, RevPAR, revenue by channel, customer segment, and category | `05_SD_Module/outputs/sd_report.md` |
| MM | Purchase spend, vendor delay rate, on-time delivery, reorder alerts, inventory risk | `06_MM_Module/outputs/mm_report.md` |
| Forecasting | Revenue baseline comparison and separately labeled cash collection forecast | `07_Analytics_Forecasting/outputs/forecast_report.md` |
| BI | Static HTML dashboard with formatted KPI cards, SVG charts, and report links | `08_BI_Integration/dashboard/index.html` |

## Data Model

The data is deterministic, synthetic, and intentionally small enough for GitHub review while covering ERP-style activity across multiple process areas.

- Master data: customers, vendors, calendar
- FI / revenue: customer invoices, customer payments, sales revenue
- CO: cost center budget and actuals
- MM: procurement vendor records and inventory movements

The generator uses a fixed seed in `scripts/generate_synthetic_data.py` and writes raw and processed CSV files. The repository avoids `.db`, `.sqlite`, `.xlsx`, `.pbix`, screenshots, archives, and other binary outputs.

## How to Run

```bash
python run_all.py
```

Run tests:

```bash
pytest
```

The pipeline uses only the Python standard library. `pytest` is used for test execution.

## Important Findings to Review

After running the pipeline, start with:

1. `09_Documentation/final_executive_summary.md`
2. `09_Documentation/final_project_report.md`
3. `08_BI_Integration/dashboard/index.html`
4. Module reports in `03_FI_Module/outputs/`, `04_CO_Module/outputs/`, `05_SD_Module/outputs/`, and `06_MM_Module/outputs/`

The reports identify aged receivables requiring follow-up, cost centers with unfavorable variance, channel and segment revenue patterns, vendor delay risk, inventory reorder risk, and directional baseline forecasts.

## SQL Support

SQL table definitions are in `02_Data/sql/schema.sql`. Example business-analysis queries for FI, CO, SD, MM, and executive KPI review are in `02_Data/sql/example_analysis_queries.sql`. The repository intentionally does not create a database file.

## Project Structure

```text
01_Project_Foundation/        Scope and SAP-inspired module mapping
02_Data/                      Raw/processed CSV data and SQL scripts
03_FI_Module/                 Financial Accounting analysis outputs
04_CO_Module/                 Controlling analysis outputs
05_SD_Module/                 Sales and Distribution analysis outputs
06_MM_Module/                 Materials Management analysis outputs
07_Analytics_Forecasting/     Forecasting outputs and metrics
08_BI_Integration/            HTML dashboard
09_Documentation/             KPI summary and final reports
scripts/                      Data generation, validation, and analytics pipeline
run_all.py                    One-command project runner
```

## Limitations

- Synthetic/anonymized data only.
- SAP S/4HANA-inspired structure only; not a real SAP implementation.
- Forecasting is deliberately simple and not production-grade.
- No live ERP connection, reservations system, tax engine, MRP run, cost allocations, or real vendor/customer records.

## Author

Ashek Alahi — Accounting, Finance, ERP Systems, and Business Analytics portfolio project.
