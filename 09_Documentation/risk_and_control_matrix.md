# ERP Risk and Control Matrix

| Risk | Related module | Data evidence | KPI/report used | Business impact | Control or management action |
| --- | --- | --- | --- | --- | --- |
| Future payments incorrectly counted as current cash | FI | Payment dates after 2025-12-31 | Collection rate, cash collection forecast | Overstated collections and understated AR | Apply as-of-date filter to FI actuals and label later payments separately. |
| Invoice status not aligned with payment status | FI | Source invoice status says Open while payments exist | Invoice status summary | Misleading collector priorities | Recalculate status from paid amount as of date and due date. |
| Overdue AR risk | FI | Outstanding invoices by aging bucket | AR aging and overdue receivables | Cash flow pressure and write-off exposure | Prioritize dunning, disputes, and credit-control review. |
| Cost center overspending | CO | Actual cost above budget | Cost center variance | Margin erosion | Department variance review and corrective action ownership. |
| Vendor delay risk | MM | Received date after promised date | Vendor delay rate | Service disruption risk | Supplier corrective action or alternate source review. |
| Inventory stock gap risk | MM | `reorder_point - closing_stock` | Inventory risk summary | Stockout risk in guest-facing operations | Expedite high-gap items and review reorder thresholds. |
| Overreliance on forecast baseline | Analytics | Holdout MAPE and MAE | Forecast metrics | Overconfident planning decisions | Treat forecasts as simple baselines and investigate large variances. |
| Revenue concentration by channel | SD | Revenue by channel | Channel report | Margin and demand concentration risk | Review direct/OTA/corporate mix. |
| Simplified synthetic data risk | All | Deterministic prototype data | Scope notes | Misinterpretation as live ERP evidence | State synthetic data, no confidential data, and not a real SAP implementation. |
