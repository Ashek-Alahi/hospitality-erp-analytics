# FI Analysis Report

Synthetic/anonymized SAP S/4HANA-inspired hospitality ERP analytics prototype. This is not a real SAP implementation.

## Key findings
Collection rate as of 2025-12-31 is 78.8% and open AR is 2,055,815.54.

## As-of-date logic
FI receivables and collection KPIs are calculated as of 2025-12-31. Payments after this date are not counted as collected cash for the as-of-date position.

## Invoice status logic
Statuses are recalculated from invoice amount, payments posted on or before the as-of date, and due date; the generated source status column is not used for reporting.

## Invoice status summary
| calculated_status_as_of | invoice_count | invoice_amount | paid_amount_as_of | outstanding_balance_as_of |
| --- | --- | --- | --- | --- |
| Cleared | 93 | 5455522.0 | 5455522.0 | 0.0 |
| Partially Paid | 77 | 3009476.55 | 2167434.71 | 842041.84 |
| Open - Not Yet Due | 8 | 512414.25 | 0.0 | 512414.25 |
| Open - Overdue | 14 | 701359.45 | 0.0 | 701359.45 |

## AR aging
| aging_bucket | outstanding_balance |
| --- | --- |
| Current | 512414.25 |
| 1-30 | 235384.0 |
| 31-60 | 154862.48 |
| 61-90 | 134761.85 |
| 90+ | 1018392.96 |

## Business meaning
Finance should prioritize overdue and partially paid accounts, validate disputed balances, and tighten credit-control follow-up cadence.

## ERP/SAP relevance
This mirrors FI-AR working-capital monitoring: invoices, clearings, due dates, and dunning priorities are transformed into management KPIs.

## Limitations
Synthetic data only; no tax, bank statement, lockbox, credit memo, or real customer dispute workflow is modeled.
