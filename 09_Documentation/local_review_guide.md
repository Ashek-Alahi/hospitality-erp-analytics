# Local Review Guide

## Run the project
```bash
python run_all.py
```
This regenerates deterministic data, validates inputs, and writes reports, charts, KPI summaries, the executive action register, and the dashboard.

## Run tests
```bash
pytest
```
The tests verify required data, pipeline execution, key outputs, calculations, documentation, and blocked binary artifacts.

## Files to open first
1. `README.md`
2. `09_Documentation/final_project_report.md`
3. `09_Documentation/executive_action_register.md`
4. `08_BI_Integration/dashboard/index.html`
5. `09_Documentation/kpi_formula_catalog.md`

## Review the dashboard
Open `08_BI_Integration/dashboard/index.html` in a browser. It is static HTML and uses only local Markdown/CSV/SVG outputs.

## Review SQL
Open `02_Data/sql/schema.sql`, `02_Data/sql/load_data.sql`, and `02_Data/sql/example_analysis_queries.sql` to see how the CSV data can be reviewed in a relational database.

## Screen-share explanation flow
Start with the README scope note, show the dashboard, open the executive action register, then drill into FI, CO, SD, MM, and forecasting reports. End with tests to prove the pipeline is reproducible.

## Troubleshooting notes
- If outputs look stale, rerun `python run_all.py`.
- If tests fail after editing data fields, check `scripts/validate_data.py` required columns.
- If a browser blocks local links, open the linked Markdown files directly from the repository.
- Do not add binary dashboard exports; keep the project GitHub-reviewable.
