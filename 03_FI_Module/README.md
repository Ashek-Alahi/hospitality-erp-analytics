# FI Module — Financial Accounting Analytics

## Business purpose
This module translates synthetic hospitality receivables, payment, and revenue data into a finance view of cash collection and open customer balances.

## Input files used
- `02_Data/processed/sales_revenue_clean.csv`
- `02_Data/processed/customer_invoices_clean.csv`
- `02_Data/processed/customer_payments_clean.csv`

## Analysis performed
- Monthly net revenue trend analysis.
- Accounts receivable aging by overdue bucket.
- Monthly customer cash collection summary.

## Output files generated
- `03_FI_Module/outputs/fi_report.md`
- `03_FI_Module/outputs/ar_aging.csv`
- `03_FI_Module/outputs/revenue_trend.csv`
- `03_FI_Module/outputs/cash_collections.csv`
- `03_FI_Module/outputs/revenue_trend.svg`

## ERP/SAP relevance
The module is inspired by SAP FI reporting concepts such as customer invoices, incoming payments, receivables aging, and finance period reporting. It does not represent a real SAP configuration.

## Management decisions supported
- Prioritize collection follow-up for older receivable buckets.
- Compare revenue activity with actual cash receipts.
- Discuss working-capital pressure in finance review meetings.
