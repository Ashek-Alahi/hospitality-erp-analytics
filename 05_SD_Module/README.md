# SD Module - Hospitality Revenue Analytics

This module models SAP S/4HANA-inspired sales and distribution analytics for hospitality commercial management. It summarizes revenue by category, sales channel, and customer segment.

## Analytics covered
- Revenue categories: Rooms, Food & Beverage, Events, Other
- Sales channels: Direct, OTA, Corporate Contract, Group Sales
- Customer segments from customer master data
- Occupancy rate
- ADR
- RevPAR

## Business value
Revenue managers can review channel mix, segment concentration, direct-booking opportunities, and hospitality operating KPIs.

## Outputs generated
- `outputs/revenue_by_category.csv`
- `outputs/revenue_by_channel.csv`
- `outputs/customer_segment_revenue.csv`
- `outputs/hospitality_kpis.csv`
- `outputs/sd_report.md`

## Limitations
Synthetic data only; no reservation engine, cancellation logic, commissions, loyalty tiers, or daily room-type inventory is modeled.
