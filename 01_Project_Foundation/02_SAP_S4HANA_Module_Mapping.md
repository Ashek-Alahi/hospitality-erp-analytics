# SAP S/4HANA-Inspired Module Mapping

This mapping explains how the prototype represents ERP concepts without claiming a live SAP implementation.

| Business area | SAP-inspired module | Prototype dataset | Prototype output | SAP/S4HANA concept represented | Management question supported | What the repo does NOT claim |
| --- | --- | --- | --- | --- | --- | --- |
| Customer invoice | FI-AR | `customer_invoices_clean.csv` | `ar_aging.csv` | Customer invoice due-date monitoring | Which invoices remain open? | No real SAP documents or extraction. |
| Incoming payment | FI-AR | `customer_payments_clean.csv` | `cash_collections.csv` | Incoming payment and clearing concept | Are invoices converting to cash? | No bank integration or payment clearing engine. |
| AR aging | FI-AR | Invoices plus payments | `overdue_receivables_summary.csv` | Aging buckets and collection monitoring | Which balances need follow-up? | No dunning configuration. |
| Collection monitoring | FI-AR | Invoices plus payments | `kpi_summary.csv` | Collection-rate KPI | Is working capital improving? | No real credit management workflow. |
| Cost center | CO | `cost_center_budget_actual_clean.csv` | `cost_center_variance.csv` | Cost center planning and actuals | Which departments overspent? | No allocation cycles or universal journal. |
| Budget actual | CO | `cost_center_budget_actual_clean.csv` | `co_report.md` | Plan/actual comparison | Are operating costs controlled? | No real controlling area setup. |
| Variance | CO | Budget and actual amounts | `cost_center_variance.csv` | Variance analysis | Which variances need action? | No production costing. |
| Profitability review | CO/FI | Sales and actual cost | `profitability_summary.csv` | Management profitability reporting | What is operating profit margin? | No legal financial statements. |
| Sales/revenue transaction | SD | `sales_revenue_clean.csv` | `revenue_by_category.csv` | Billing/revenue analytics concept | What revenue was generated? | No sales order or billing document evidence. |
| Customer master | SD | `customers_clean.csv` | `customer_segment_revenue.csv` | Customer segment enrichment | Which segments drive revenue? | No real customer master data. |
| Channel | SD | `sales_revenue_clean.csv` | `revenue_by_channel.csv` | Sales channel reporting | Is revenue concentrated? | No commission settlement. |
| Revenue category | SD | `sales_revenue_clean.csv` | `hospitality_kpis.csv` | Rooms/F&B/events revenue view | How are hotel KPIs performing? | No property-management-system integration. |
| Vendor master | MM | `vendors_clean.csv` | `vendor_performance.csv` | Vendor evaluation | Which vendors are delayed? | No real supplier records. |
| Purchase order | MM | `procurement_vendor_clean.csv` | `purchase_spend.csv` | Purchasing transaction concept | Where is spend concentrated? | No SAP PO numbers or releases. |
| Delivery timing | MM | Promised and received dates | `vendor_performance.csv` | Goods receipt timing | Are suppliers reliable? | No warehouse execution. |
| Goods receipt concept | MM | `procurement_vendor_clean.csv` | `vendor_performance.csv` | Receipt monitoring | Which deliveries were late? | No three-way match. |
| Inventory monitoring | MM | `inventory_movements_clean.csv` | `reorder_alerts.csv` | Reorder point exception | Which items need replenishment? | No MRP run. |
| KPI summary | Analytics | Module outputs | `kpi_summary.md` | Embedded analytics concept | What are the executive KPIs? | No SAP Fiori app. |
| Exception monitoring | Analytics | AR, variance, vendor, inventory outputs | `executive_action_register.md` | Management-by-exception | What needs action? | No workflow approvals. |
| Baseline forecasting | Analytics | Monthly revenue and collections | `forecast_metrics.csv` | Planning support | Which baseline is safest to discuss? | Not production-grade forecasting. |
| Executive dashboard | Analytics | KPI/action outputs | `dashboard/index.html` | BI-style reporting | What should leaders review first? | No Power BI `.pbix` or SAP Analytics Cloud model. |
