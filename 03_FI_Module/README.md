# FI Module - Invoice-to-Cash Analytics

This module models an SAP S/4HANA-inspired FI-AR invoice-to-cash scenario using synthetic hospitality invoices and payments. It covers invoices, payments, AR aging, collection rate, open AR, and recalculated invoice status.

## As-of-date logic
FI receivables and collection KPIs are calculated as of 2025-12-31. Payments after this date are not counted as collected cash for the as-of-date position. Future-dated synthetic payments remain in the source data but are treated as later cash events.

## Invoice status logic
Invoice status is calculated from paid amount as of 2025-12-31 and due date: Cleared, Partially Paid, Open - Not Yet Due, or Open - Overdue. The generated source `status` field is not used as the reporting status.

## Business value
Credit control can focus on overdue exposure, partially paid accounts, and open AR rather than a misleading all-open status list.

## Outputs generated
- `outputs/ar_aging.csv`
- `outputs/overdue_receivables_summary.csv`
- `outputs/invoice_status_summary.csv`
- `outputs/invoice_status_detail.csv`
- `outputs/cash_collections.csv`
- `outputs/fi_report.md`

## Limitations
Synthetic data only; not a real SAP implementation. No tax, bank statement matching, lockbox, credit memo, or dispute workflow is modeled.
