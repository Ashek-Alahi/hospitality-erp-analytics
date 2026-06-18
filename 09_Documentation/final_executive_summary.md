# Final Executive Summary

Synthetic/anonymized SAP S/4HANA-inspired hospitality ERP analytics prototype. This is not a real SAP implementation.

## Portfolio positioning
A SAP S/4HANA-inspired hospitality ERP analytics prototype using deterministic synthetic data, Python, SQL-ready CSVs, Markdown reporting, SVG charts, and an HTML dashboard.

## Most important findings
| kpi | value |
| --- | --- |
| Total net revenue | 12867010.04 |
| Occupancy rate pct | 86.45 |
| ADR | 126.0 |
| RevPAR | 108.93 |
| Collection rate pct as of 2025-12-31 | 78.76 |
| Open AR balance as of 2025-12-31 | 2055815.54 |
| Overdue AR exposure | 1543401.29 |
| Operating profit | 7327642.68 |
| Operating profit margin pct | 56.95 |
| Purchase spend | 1185479.52 |
| Vendor delay rate pct | 49.17 |
| Reorder alerts | 113 |
| Items at risk | 5 |
| Max inventory stock gap | 300.0 |
| Best forecast baseline | linear trend forecast |

## Recommended actions
| action_id | module | issue | evidence | priority | recommended_action | owner_role | expected_business_value |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ACT-001 | FI | Overdue receivables as of date | Open AR balance 2,055,815.54 | High | Prioritize overdue and partially paid receivables using as-of-date invoice status and aging. | Finance / Credit Control | Improve cash conversion and reduce write-off exposure. |
| ACT-002 | MM | High vendor delay rate | GuestTech Supplies delay rate 70.83% | High | Review service levels, expedite open items, and identify alternate suppliers for critical categories. | Procurement Manager | Protect guest service levels and reduce emergency purchasing. |
| ACT-003 | MM | Inventory stock gap risk | 113 reorder alerts generated | High | Replenish high stock-gap items and confirm reorder points for seasonal demand. | Inventory Controller | Reduce stockout risk in housekeeping, F&B, and maintenance operations. |
| ACT-004 | CO | Unfavorable cost center variance | Food & Beverage variance 4.59% | Medium | Review spending drivers and update department action plans. | Department Manager / Controller | Improve budget accountability without reducing service quality. |
| ACT-005 | SD | Revenue concentration by channel | Top channel is Direct at 4,137,754.59 | Medium | Review direct booking, negotiated account, and OTA channel mix. | Revenue Manager | Reduce margin pressure and strengthen commercial resilience. |
| ACT-006 | Forecasting | Weak forecast reliability | Best baseline linear trend forecast MAPE 9.74% | Medium | Use baseline forecasts as planning signals and investigate large variances before commitments. | FP&A / Revenue Management | Improve short-term planning discipline while avoiding overconfidence. |

## Scope note
This is synthetic-data-based, not a real SAP implementation, and not production-grade forecasting.
