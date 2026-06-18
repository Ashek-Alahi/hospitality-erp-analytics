# FI Analysis Report

Synthetic/anonymized SAP S/4HANA-inspired hospitality ERP analytics prototype. This is not a real SAP implementation.

## Key findings
Collection rate is 82.4% and open AR is 1,705,443.94. The aging profile intentionally includes 31-60, 61-90, and 90+ day exposure for credit-control review.

## AR aging
| aging_bucket | outstanding_balance |
| --- | --- |
| Current | 187148.12 |
| 1-30 | 220334.55 |
| 31-60 | 144806.46 |
| 61-90 | 134761.85 |
| 90+ | 1018392.96 |

## Business meaning
Finance should prioritize 90+ and 61-90 day accounts, validate disputed balances, and tighten follow-up cadence for group/event and contract receivables.

## ERP/SAP relevance
This mirrors FI-AR working-capital monitoring: invoices, clearings, due dates, and dunning priorities are transformed into management KPIs.

## Limitations
Synthetic data only; no tax, bank statement, lockbox, credit memo, or real customer dispute workflow is modeled.
