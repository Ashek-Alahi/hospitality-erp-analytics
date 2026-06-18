# Analytics and Forecasting Report

Synthetic/anonymized SAP S/4HANA-inspired hospitality ERP analytics prototype.

## Revenue forecast
| period | net_revenue | forecast_revenue | absolute_error |
| --- | --- | --- | --- |
| 2025-07 | 381763.59 | 330365.84 | 51397.75 |
| 2025-08 | 379286.07 | 311539.11 | 67746.96 |
| 2025-09 | 309965.48 | 292712.38 | 17253.1 |
| 2025-10 | 273885.65 | 273885.65 | 0.0 |
| 2025-11 | 274610.12 | 255058.92 | 19551.2 |
| 2025-12 | 430348.27 | 236232.19 | 194116.08 |

## Evaluation metrics
| model | holdout_months | mape_pct | mae |
| --- | --- | --- | --- |
| Revenue linear trend baseline | 2 | 26.11 | 106833.64 |
| Cash collection 3-month moving average | 0 | n/a | n/a |

## Cash-flow forecast
| period | payment_amount | forecast_cash_collection |
| --- | --- | --- |
| 2025-06 | 78421.94 | 97924.09 |
| 2025-07 | 89365.23 | 81835.11 |
| 2025-08 | 109564.89 | 81998.6 |
| 2025-09 | 109798.36 | 92450.69 |
| 2025-10 | 89773.25 | 102909.49 |
| 2025-11 | 78643.43 | 103045.5 |
