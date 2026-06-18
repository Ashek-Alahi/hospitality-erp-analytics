# MM Analysis Report

Synthetic/anonymized SAP S/4HANA-inspired hospitality ERP analytics prototype. This is not a real SAP implementation.

## Key findings
There are 113 reorder alerts. Highest vendor delay rate: GuestTech Supplies at 70.83%.

## Vendor performance
| vendor_id | vendor_name | purchase_amount | avg_delivery_delay_days | vendor_delay_rate_pct | on_time_delivery_pct |
| --- | --- | --- | --- | --- | --- |
| V001 | FreshFields Produce | 286547.83 | 0.29 | 20.83 | 79.17 |
| V002 | LinenPro Services | 235060.06 | 0.62 | 45.83 | 54.17 |
| V003 | GuestTech Supplies | 212206.52 | 2.21 | 70.83 | 29.17 |
| V004 | Beverage Central | 213529.34 | 0.5 | 37.5 | 62.5 |
| V005 | EcoAmenity Co | 238135.77 | 2.42 | 70.83 | 29.17 |

## Reorder alerts
| period | item_id | item_name | category | closing_stock | reorder_point |
| --- | --- | --- | --- | --- | --- |
| 2024-01 | I002 | Coffee beans | Food & Beverage | 51 | 75 |
| 2024-01 | I004 | HVAC filters | Maintenance | 45 | 45 |
| 2024-02 | I003 | Guest shampoo | Guest Supplies | 154 | 240 |
| 2024-02 | I004 | HVAC filters | Maintenance | 12 | 45 |
| 2024-02 | I005 | Bottled water | Food & Beverage | 201 | 300 |
| 2024-03 | I002 | Coffee beans | Food & Beverage | 0 | 75 |
| 2024-03 | I003 | Guest shampoo | Guest Supplies | 87 | 240 |
| 2024-03 | I004 | HVAC filters | Maintenance | 0 | 45 |
| 2024-03 | I005 | Bottled water | Food & Beverage | 206 | 300 |
| 2024-04 | I002 | Coffee beans | Food & Beverage | 0 | 75 |
| 2024-04 | I003 | Guest shampoo | Guest Supplies | 42 | 240 |
| 2024-04 | I004 | HVAC filters | Maintenance | 22 | 45 |
| 2024-04 | I005 | Bottled water | Food & Beverage | 142 | 300 |
| 2024-05 | I001 | Bath linen | Housekeeping | 111 | 180 |
| 2024-05 | I002 | Coffee beans | Food & Beverage | 0 | 75 |
| 2024-05 | I003 | Guest shampoo | Guest Supplies | 0 | 240 |
| 2024-05 | I004 | HVAC filters | Maintenance | 0 | 45 |
| 2024-05 | I005 | Bottled water | Food & Beverage | 86 | 300 |
| 2024-06 | I001 | Bath linen | Housekeeping | 107 | 180 |
| 2024-06 | I002 | Coffee beans | Food & Beverage | 0 | 75 |

## Management recommendations
Expedite high-risk items below reorder point and review delayed vendors for service-level corrective action or alternate sourcing.

## ERP/SAP relevance
This reflects MM purchasing, goods receipt timing, vendor evaluation, and inventory replenishment monitoring.

## Limitations
No MRP run, safety-stock optimization, batch expiry, or purchase-price variance accounting is modeled.
