# CO Analysis Report

Synthetic/anonymized SAP S/4HANA-inspired hospitality ERP analytics prototype. This is not a real SAP implementation.

## Key findings
Operating profit margin is 56.9%. Highest unfavorable variance: Food & Beverage at 4.6%.

## Budget variance ranking
| cost_center_id | cost_center_name | budget_amount | actual_amount | variance | variance_pct |
| --- | --- | --- | --- | --- | --- |
| CC200 | Food & Beverage | 1031184.0 | 1078481.93 | 47297.93 | 4.59 |
| CC100 | Rooms | 1939608.0 | 1953070.07 | 13462.07 | 0.69 |
| CC400 | Maintenance | 515592.0 | 525495.83 | 9903.83 | 1.92 |
| CC300 | Housekeeping | 736560.0 | 739726.76 | 3166.76 | 0.43 |
| CC500 | Sales & Marketing | 589248.0 | 586508.62 | -2739.38 | -0.46 |
| CC600 | Administration | 662904.0 | 656084.15 | -6819.85 | -1.03 |

## Management recommendations
Review departments with positive variance first and document corrective actions without reducing service quality.

## ERP/SAP relevance
The analysis resembles CO cost center planning versus actual postings and profitability review.

## Limitations
No allocation cycles, internal orders, activity types, or product/customer profitability ledgers are modeled.
