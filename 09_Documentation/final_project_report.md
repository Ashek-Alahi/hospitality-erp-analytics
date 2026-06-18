# Final Project Report

## Objective

Build a completed, portfolio-grade hospitality ERP analytics MVP using synthetic data and text-based deliverables only.

## Scope

- FI: AR aging, revenue trends, outstanding balance, and cash collections.
- CO: budget vs actual, cost center variance, and profitability.
- SD: sales performance by revenue category, channel, and segment.
- MM: purchase spend, vendor performance, stock movement, and reorder alerts.
- Analytics: revenue and cash-flow forecasting baselines with evaluation metrics.
- BI: HTML dashboard and guidance for Power BI connection to CSV outputs.

## Data Model

The model uses CSV master data and transaction-like tables for customers, vendors, sales, invoices, payments, cost centers, purchase orders, inventory movements, and calendar dates. SQL DDL and import scripts are provided in `02_Data/sql/` for users who want to create their own local SQLite database.

## Reproducibility

Run `python run_all.py` from the repository root to regenerate reports, KPI tables, SVG charts, and the HTML dashboard.
