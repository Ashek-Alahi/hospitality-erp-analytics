# MM Module - Procurement and Inventory Risk Analytics

This module models SAP S/4HANA-inspired materials management analytics for procurement reliability and stockout control.

## Analytics covered
- Purchase spend by category
- Vendor delivery delay and on-time performance
- Reorder alerts
- Inventory risk summary using stock gap: `reorder_point - closing_stock`

## Business value
Procurement and inventory teams can identify delayed vendors, expedite items below reorder point, and prioritize categories with the largest stock gaps.

## Outputs generated
- `outputs/purchase_spend.csv`
- `outputs/vendor_performance.csv`
- `outputs/reorder_alerts.csv`
- `outputs/inventory_risk_summary.csv`
- `outputs/mm_report.md`

## Limitations
Synthetic data only; no MRP run, safety-stock optimization, batch expiry, purchase-price variance accounting, or supplier contract workflow is modeled.
