# Business Scenario

## Context
The fictional hospitality group operates several city and resort properties with rooms, food and beverage, events, and ancillary revenue streams. Management wants a reliable cross-module reporting view without implying a live ERP deployment.

## Disconnected reporting problem
Finance tracks invoices and payments, revenue management tracks room and channel performance, procurement tracks vendor activity, operations tracks stock levels, and controllers track cost-center budgets. When these views are disconnected, leaders cannot easily connect sales activity to cash, cost control, vendor reliability, and inventory risk.

## Pain points
- Finance: overdue receivables, collection-rate visibility, and cash planning discipline.
- Sales: channel concentration, customer-segment mix, ADR, RevPAR, and occupancy review.
- Procurement: vendor delivery delays and purchase spend by category.
- Inventory: items below reorder point that can affect service levels.
- Cost control: unfavorable budget variance and department accountability.

## Why cross-module ERP reporting is needed
Hospitality decisions are process-driven. A booking may create revenue, an invoice may remain unpaid, a supplier delay may create operational risk, and cost-center overspending may reduce margin. Cross-module reporting provides one management view across these dependencies.

## How the prototype addresses the problem
The project generates deterministic synthetic ERP-style CSV data, validates the data, calculates FI/CO/SD/MM KPIs, creates forecasts, writes module reports, produces SQL examples, and publishes a static dashboard plus an executive action register.

## Decisions supported
- Which receivables should finance prioritize?
- Which departments require budget review?
- Which channels and segments deserve commercial focus?
- Which vendors or inventory items require action?
- Which forecast baseline is appropriate for planning discussion?
