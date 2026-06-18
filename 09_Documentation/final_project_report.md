# Final Project Report

Synthetic/anonymized SAP S/4HANA-inspired hospitality ERP analytics prototype. This is not a real SAP implementation.

## Business problem
Hospitality leaders need one management view connecting commercial performance, receivables, cost-center accountability, purchasing reliability, inventory risk, and short-term planning.

## Project objective
Build a GitHub-reviewable analytics prototype that converts deterministic synthetic ERP-style CSV data into FI, CO, SD, MM, forecasting, KPI, SQL, and dashboard outputs.

## Data model summary
Customer, vendor, and calendar master data connect to sales revenue, invoices, payments, cost-center actuals, procurement records, and inventory movements.

## FI findings
Collection rate is 78.8% as of 2025-12-31 with open AR of 2,055,815.54; payments after the as-of date are excluded from actual cash and invoice status.

## Invoice status findings
| calculated_status_as_of | invoice_count | invoice_amount | paid_amount_as_of | outstanding_balance_as_of |
| --- | --- | --- | --- | --- |
| Cleared | 93 | 5455522.0 | 5455522.0 | 0.0 |
| Partially Paid | 77 | 3009476.55 | 2167434.71 | 842041.84 |
| Open - Not Yet Due | 8 | 512414.25 | 0.0 | 512414.25 |
| Open - Overdue | 14 | 701359.45 | 0.0 | 701359.45 |

## CO findings
Operating profit margin is 56.9%. The largest unfavorable variance is Food & Beverage at 4.6%.

## SD findings
Occupancy is 86.5%, ADR is 126.00, and RevPAR is 108.93.

## MM findings
The prototype identifies 113 reorder alerts using stock-gap risk and vendor delivery variation.

## Forecasting findings
Revenue output separates actual, holdout, and true future forecast rows; linear trend forecast has the best holdout MAPE at 9.74%.

## Executive KPI summary
| kpi | value |
| --- | --- |
| Total net revenue | 12867010.04 |
| Occupancy rate pct | 86.45 |
| ADR | 126.0 |
| RevPAR | 108.93 |
| Collection rate pct as of 2025-12-31 | 78.76 |
| Open AR balance as of 2025-12-31 | 2055815.54 |
| Overdue AR exposure | 1543401.29 |
| Operating profit | 7327642.68 |
| Operating profit margin pct | 56.95 |
| Purchase spend | 1185479.52 |
| Vendor delay rate pct | 49.17 |
| Reorder alerts | 113 |
| Items at risk | 5 |
| Max inventory stock gap | 300.0 |
| Best forecast baseline | linear trend forecast |

## Management recommendations
Prioritize overdue AR follow-up, review unfavorable cost-center variances, refine channel strategy, act on stock gaps, and review delayed vendors.

## SAP/ERP relevance
The design is inspired by SAP S/4HANA process areas, master data, transactional documents, exception monitoring, and management reporting while remaining a portfolio analytics prototype.

## Limitations
No live SAP connection, no confidential data, no binary BI file, and simplified business logic. Forecasts are directional baselines, not production commitments.
