# Final Project Report

Synthetic/anonymized SAP S/4HANA-inspired hospitality ERP analytics prototype. This is not a real SAP implementation.

## Business problem
Hospitality leaders need one management view connecting commercial performance, receivables, cost-center accountability, purchasing reliability, inventory risk, and short-term planning.

## Project objective
Build a GitHub-reviewable analytics prototype that converts deterministic synthetic ERP-style CSV data into FI, CO, SD, MM, forecasting, KPI, SQL, and dashboard outputs.

## Data model summary
Customer, vendor, and calendar master data connect to sales revenue, customer invoices, customer payments, cost-center actuals, procurement records, and inventory movements. The model is intentionally small, auditable, and text-based.

## FI findings
Collection rate is 82.4% with open AR of 1,705,443.94. Aging buckets include current, 1-30, 31-60, 61-90, and 90+ day exposure for credit-control prioritization.

## CO findings
Operating profit margin is 56.9%. The largest unfavorable cost-center variance is Food & Beverage at 4.6%.

## SD findings
Occupancy is 86.5%, ADR is 126.00, and RevPAR is 108.93. Channel and segment summaries show where revenue concentration should be reviewed.

## MM findings
The prototype identifies 113 reorder alerts and vendor delivery variation. Highest vendor delay rate is GuestTech Supplies at 70.83%.

## Forecasting findings
Revenue baselines compare naive, moving-average, and linear-trend methods; linear trend forecast has the best three-month holdout MAPE at 9.74%. Cash collection forecasting is labeled separately and uses a three-month moving average.

## Executive KPI summary
| kpi | value |
| --- | --- |
| Total net revenue | 12867010.04 |
| Occupancy rate pct | 86.45 |
| ADR | 126.0 |
| RevPAR | 108.93 |
| Collection rate pct | 82.38 |
| Open AR balance | 1705443.94 |
| Operating profit | 7327642.68 |
| Operating profit margin pct | 56.95 |
| Purchase spend | 1185479.52 |
| Vendor delay rate pct | 49.17 |
| Reorder alerts | 113 |
| Best forecast baseline | linear trend forecast |

## Management recommendations
Prioritize overdue AR follow-up, review unfavorable cost-center variances, refine channel and segment strategy, act on reorder alerts, and review delayed vendors before service levels are affected.

## SAP/ERP relevance
The design is inspired by SAP S/4HANA process areas, master data, transactional documents, exception monitoring, and management reporting while remaining a portfolio analytics prototype.

## Limitations
No live SAP connection, no confidential data, no binary BI file, and simplified business logic. Forecasts are directional baselines, not production commitments.
