# CO Module — Controlling and Profitability Analytics

## Business purpose
This module shows how hospitality managers can monitor cost center spending against budget and connect operating cost to profitability.

## Input files used
- `02_Data/processed/cost_center_budget_actual_clean.csv`
- `02_Data/processed/sales_revenue_clean.csv`

## Analysis performed
- Budget versus actual cost by cost center.
- Variance calculation for each cost center.
- Total net revenue, operating cost, and operating profit summary.

## Output files generated
- `04_CO_Module/outputs/co_report.md`
- `04_CO_Module/outputs/cost_center_variance.csv`
- `04_CO_Module/outputs/profitability_summary.csv`
- `04_CO_Module/outputs/cost_center_actuals.svg`

## ERP/SAP relevance
The module is inspired by SAP CO cost center accounting and profitability review. It demonstrates how budgeted and actual cost records can support monthly control activities.

## Management decisions supported
- Identify departments requiring cost-control action.
- Review whether revenue levels cover operating cost.
- Support budget discussions using variance evidence.
