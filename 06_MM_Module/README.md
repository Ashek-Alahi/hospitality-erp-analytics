# MM Module — Procurement and Inventory Analytics

## Business purpose
This module provides a procurement and stock-control view for hospitality operations, where vendor reliability and inventory availability affect service continuity.

## Input files used
- `02_Data/processed/procurement_vendor_clean.csv`
- `02_Data/processed/vendors_clean.csv`
- `02_Data/processed/inventory_movements_clean.csv`

## Analysis performed
- Purchase spend by procurement category.
- Vendor spend and average delivery delay.
- Reorder alerts where closing stock is at or below reorder point.

## Output files generated
- `06_MM_Module/outputs/mm_report.md`
- `06_MM_Module/outputs/purchase_spend.csv`
- `06_MM_Module/outputs/vendor_performance.csv`
- `06_MM_Module/outputs/reorder_alerts.csv`
- `06_MM_Module/outputs/purchase_spend.svg`

## ERP/SAP relevance
The module is inspired by SAP MM processes such as purchasing, vendor master data, goods receipt timing, and inventory monitoring.

## Management decisions supported
- Negotiate with vendors based on spend and delivery performance.
- Prioritize replenishment for items below reorder threshold.
- Review procurement category exposure and supply risk.
