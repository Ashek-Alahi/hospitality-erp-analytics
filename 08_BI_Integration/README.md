# BI Integration

The dashboard layer is text-based and GitHub-reviewable.

- HTML dashboard: `08_BI_Integration/dashboard/index.html`
- Source KPI output: `09_Documentation/kpi_summary.csv`
- Chart files: SVG outputs under each module's `outputs/` folder

## Power BI Guidance

Power BI can connect directly to the CSV files in `02_Data/processed/` and output CSV files in each module folder. Use **Get Data > Text/CSV**, load the files, then create relationships using customer, vendor, period, and date fields. This repository intentionally does not include a `.pbix` file because binary report files are outside the project rules.
