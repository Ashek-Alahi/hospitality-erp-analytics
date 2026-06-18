# SAP S/4HANA-Inspired Module Mapping

This repository is a hospitality ERP analytics prototype inspired by SAP S/4HANA business processes. It is not an SAP S/4HANA implementation and does not contain SAP configuration, SAP tables, or non-public enterprise data.

| Prototype area | SAP-inspired module concept | Repository evidence | Business question supported |
| --- | --- | --- | --- |
| Financial Accounting | FI accounts receivable, revenue recognition view, and collections monitoring | `03_FI_Module/outputs/fi_report.md`, `customer_invoices_clean.csv`, `customer_payments_clean.csv` | How much revenue was generated, how much cash was collected, and where are receivables aging? |
| Controlling | CO cost center planning, actual cost tracking, and profitability | `04_CO_Module/outputs/co_report.md`, `cost_center_budget_actual_clean.csv` | Which departments are over or under budget, and what is the operating profit view? |
| Sales and Distribution | SD sales channels, revenue categories, customer segmentation | `05_SD_Module/outputs/sd_report.md`, `sales_revenue_clean.csv`, `customers_clean.csv` | Which channels, services, and customer segments contribute most to revenue? |
| Materials Management | MM procurement, vendor performance, inventory reorder monitoring | `06_MM_Module/outputs/mm_report.md`, `procurement_vendor_clean.csv`, `inventory_movements_clean.csv` | Which categories drive spend, which vendors deliver reliably, and what stock needs attention? |
| Embedded analytics concept | ERP reporting layer and baseline forecasting | `07_Analytics_Forecasting/outputs/forecast_report.md`, `08_BI_Integration/dashboard/index.html` | What KPI trends and baseline forecasts can management review from ERP-style data? |

## How the Modules Connect

- Customers connect to sales and invoices through `customer_id`.
- Invoices connect to payments through `invoice_id`.
- Vendors connect to procurement transactions through `vendor_id`.
- Period and date fields allow monthly reporting across FI, CO, SD, MM, and analytics outputs.

The design demonstrates ERP analytics thinking: master data supports transaction data, transaction data feeds module-level analysis, and module outputs feed executive reporting.
