# BI Integration

## Business purpose
This folder turns module outputs into an executive dashboard entry point that can be opened locally or reviewed as text in GitHub.

## Input files used
- `09_Documentation/kpi_summary.csv`
- SVG charts from FI, CO, SD, MM, and forecasting output folders
- Module CSV outputs for optional BI tool connection

## Analysis performed
The dashboard does not perform new calculations. It presents regenerated KPI values and embeds text-based SVG visuals produced by the Python pipeline.

## Output files generated
- `08_BI_Integration/dashboard/index.html`

## ERP/SAP relevance
The dashboard represents an ERP analytics consumption layer: finance, sales, controlling, and procurement KPIs are summarized for management review.

## Management decisions supported
- Review cross-module KPIs in one place.
- Use CSV outputs as a starting point for Power BI, Tableau, Excel Power Query, or SQLite exploration.
- Discuss how ERP transaction data becomes an executive reporting layer.

## Power BI guidance
Use **Get Data > Text/CSV** to connect to files in `02_Data/processed/` and module `outputs/` folders. Create relationships using customer, vendor, period, and date fields. This repository intentionally does not include a `.pbix` file because binary report files are outside the project rules.
