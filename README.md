# Hospitality ERP Analytics Portfolio Project

A portfolio-ready **SAP S/4HANA-inspired hospitality ERP analytics prototype** using deterministic synthetic/anonymized data only. This repository does **not** claim to be a real SAP S/4HANA implementation; it demonstrates how FI, CO, SD, MM, SQL, Python, forecasting baselines, and BI-style reporting can be connected in a GitHub-reviewable analytics project.

## Business Problem

Hotel leadership needs a connected view of revenue performance, receivables, operating cost control, procurement reliability, inventory risk, and short-term planning. These topics are often reviewed in separate spreadsheets or systems, making it difficult to connect commercial decisions with working capital, service levels, and cost-center accountability.

This project converts small ERP-style CSV tables into module reports, exception outputs, SVG charts, SQL examples, and an HTML dashboard.

## What Makes This Useful for ERP / Analytics Interviews

- Shows accounting and ERP process knowledge across FI, CO, SD, and MM.
- Uses readable Python automation rather than manual spreadsheet work.
- Keeps data, reports, charts, SQL, and dashboard files text-based for GitHub review.
- Includes business exceptions instead of perfect demo data: overdue AR, vendor delays, reorder alerts, and cost-center variances.
- Explains business meaning, management action, SAP relevance, and limitations.

## ERP Module Coverage

| Module | Analytics coverage | Important outputs |
| --- | --- | --- |
| FI | AR aging, overdue receivables, collection rate, revenue trend, cash collections | `03_FI_Module/outputs/fi_report.md` |
| CO | Budget vs actual, variance percentage, unfavorable cost-center ranking, operating profit margin | `04_CO_Module/outputs/co_report.md` |
| SD | Occupancy, ADR, RevPAR, revenue by channel, customer segment, and category | `05_SD_Module/outputs/sd_report.md` |
| MM | Purchase spend, vendor delay rate, on-time delivery, reorder alerts, inventory risk | `06_MM_Module/outputs/mm_report.md` |
| Forecasting | Naive, moving average, and linear trend baseline comparison using MAPE and MAE | `07_Analytics_Forecasting/outputs/forecast_report.md` |
| BI | HTML dashboard with KPI cards, SVG charts, and report links | `08_BI_Integration/dashboard/index.html` |

## Hospitality and ERP KPIs

The pipeline generates these KPIs in `09_Documentation/kpi_summary.csv`:

- Total net revenue
- Occupancy rate
- ADR, Average Daily Rate
- RevPAR, Revenue per Available Room
- Collection rate
- Open AR balance
- Operating profit and operating profit margin
- Purchase spend
- Vendor delay rate
- Reorder alert count
- Best baseline forecast model

## Data Model

The data is deterministic, synthetic, and intentionally small enough for GitHub review while covering 24 months of activity.

- Master data: customers, vendors, calendar
- FI / revenue: customer invoices, customer payments, sales revenue
- CO: cost center budget and actuals
- MM: procurement vendor records and inventory movements

The generator uses a fixed seed in `scripts/generate_synthetic_data.py` and writes both raw and processed CSV files. No `.db`, `.sqlite`, `.xlsx`, `.pbix`, image, archive, or other binary output is required.

## How to Run

```bash
python run_all.py
```

Run tests:

```bash
pytest
```

The project uses only the Python standard library for the pipeline. `pytest` is used for test execution.

## Important Findings to Review

After running the pipeline, start with:

1. `09_Documentation/final_executive_summary.md`
2. `09_Documentation/final_project_report.md`
3. `08_BI_Integration/dashboard/index.html`
4. Module reports in `03_FI_Module/outputs/`, `04_CO_Module/outputs/`, `05_SD_Module/outputs/`, and `06_MM_Module/outputs/`

The reports identify aged receivables requiring follow-up, cost centers with unfavorable variance, channel/segment revenue patterns, vendor delay risk, and inventory reorder risk.

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
