# Final Project Report

Synthetic/anonymized SAP S/4HANA-inspired hospitality ERP analytics prototype. This is not a real SAP implementation.

## Business problem
Hospitality management needs connected visibility across revenue, receivables, cost control, procurement, inventory, and forecast planning.

## ERP module coverage
FI covers AR aging and collections; CO covers budget variance and operating margin; SD covers occupancy, ADR, RevPAR, channel, segment, and category revenue; MM covers vendor delays and reorder risk.

## KPI summary
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
Use the reports as an exception dashboard: collect aged receivables, investigate cost-center overruns, refine pricing/channel strategy, and act on vendor or reorder alerts.

## SAP relevance
The design is inspired by SAP S/4HANA process areas, master data, documents, and management reporting, but it is a portfolio prototype only.

## Limitations
No live SAP connection, no confidential data, no binary BI file, and simplified business logic.
