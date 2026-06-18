# Hospitality ERP Analytics MVP

A completed portfolio-grade, SAP S/4HANA-inspired hospitality ERP analytics prototype using synthetic/anonymized data only. This is not a real SAP implementation; it is a practical analytics project that demonstrates ERP process knowledge, SQL-ready data modeling, Python automation, and business reporting.

## Business Problem

Hospitality leaders need one view of revenue, receivables, cost control, procurement, inventory, and short-term forecasts. In many organizations these topics are reviewed separately, which makes it harder to connect sales performance, cash collection, operating cost, vendor reliability, and stock risk.

This MVP shows how ERP-style data can be organized into a decision-support layer for finance and operations.

## ERP Module Coverage

| Module | Coverage | Key outputs |
| --- | --- | --- |
| FI | AR aging, outstanding balance, revenue trend, cash collections | `03_FI_Module/outputs/fi_report.md` |
| CO | Budget vs actual, cost center variance, profitability | `04_CO_Module/outputs/co_report.md` |
| SD | Sales performance, revenue by category/channel, customer segments | `05_SD_Module/outputs/sd_report.md` |
| MM | Purchase spend, vendor performance, inventory movement, reorder alerts | `06_MM_Module/outputs/mm_report.md` |
| Analytics | Revenue forecast and cash-flow forecast baselines | `07_Analytics_Forecasting/outputs/forecast_report.md` |
| BI | HTML dashboard and Power BI CSV connection guidance | `08_BI_Integration/dashboard/index.html` |

## Repository Structure

```text
01_Project_Foundation/        Project scope and ERP module mapping notes
02_Data/                      Synthetic raw/processed CSV data and SQL scripts
03_FI_Module/                 Financial Accounting analysis and outputs
04_CO_Module/                 Controlling analysis and outputs
05_SD_Module/                 Sales and Distribution analysis and outputs
06_MM_Module/                 Materials Management analysis and outputs
07_Analytics_Forecasting/     Forecasting outputs and model metrics
08_BI_Integration/            HTML dashboard and BI instructions
09_Documentation/             Data dictionary, KPI summary, final reports
scripts/                      Reusable Python analytics pipeline
run_all.py                    One-command project runner
requirements.txt              Dependency note
```

## Data Model

The project uses CSV files that can be reviewed directly on GitHub and imported into SQLite if desired.

- Master data: `customers`, `vendors`, `calendar`
- Revenue and FI: `sales_revenue`, `customer_invoices`, `customer_payments`
- CO: `cost_center_budget_actual`
- MM: `procurement_vendor`, `inventory_movements`

SQL definitions are available in `02_Data/sql/schema.sql`, and SQLite CLI import guidance is available in `02_Data/sql/load_data.sql`. No `.db` or `.sqlite` file is included or generated.

## How to Run

```bash
python run_all.py
```

The pipeline uses only the Python standard library. Running it regenerates CSV KPI tables, Markdown reports, SVG charts, and the HTML dashboard.

## Key Outputs

| Output | Path |
| --- | --- |
| KPI summary CSV | `09_Documentation/kpi_summary.csv` |
| KPI summary Markdown | `09_Documentation/kpi_summary.md` |
| Data dictionary | `09_Documentation/data_dictionary.md` |
| Final executive summary | `09_Documentation/final_executive_summary.md` |
| Final project report | `09_Documentation/final_project_report.md` |
| HTML dashboard | `08_BI_Integration/dashboard/index.html` |
| Revenue trend SVG | `03_FI_Module/outputs/revenue_trend.svg` |
| Cost center actuals SVG | `04_CO_Module/outputs/cost_center_actuals.svg` |
| Revenue by channel SVG | `05_SD_Module/outputs/revenue_by_channel.svg` |
| Purchase spend SVG | `06_MM_Module/outputs/purchase_spend.svg` |

## Current KPI Snapshot

See `09_Documentation/kpi_summary.md` for the regenerated KPI table. The MVP highlights total net revenue, open AR balance, operating profit, purchase spend, and reorder alerts.

## Power BI Use

Use **Get Data > Text/CSV** in Power BI to connect to files in `02_Data/processed/` and module output folders. This repository does not include a `.pbix` file because the project is intentionally text-based and GitHub-reviewable.

## Data and Confidentiality Statement

All records are synthetic/anonymized sample data created for portfolio demonstration. The project does not include private company data, confidential operational data, or a claim of real SAP S/4HANA implementation.

## Author

Ashek Alahi  
Accounting, Finance, ERP Systems, and Business Analytics portfolio project.
