# Analytics and Forecasting Report

Synthetic/anonymized SAP S/4HANA-inspired hospitality ERP analytics prototype. This is not a real SAP implementation.

## Key findings
Compared naive, moving average, and linear trend baselines. Best holdout MAPE is 9.74% from linear trend forecast. Future periods begin after the latest actual revenue month.

## Revenue forecast record types
`actual` rows are training history, `holdout` rows compare baseline predictions against known actuals, and `forecast` rows are true future periods.

## Revenue forecast metrics
| model | holdout_months | mape_pct | mae |
| --- | --- | --- | --- |
| naive forecast | 3 | 14.15 | 90603.48 |
| moving average forecast | 3 | 16.93 | 103537.6 |
| linear trend forecast | 3 | 9.74 | 59202.52 |

## Cash collection forecast
| period | actual_cash_collected | forecast_cash_collected | record_type | method |
| --- | --- | --- | --- | --- |
| 2025-10 | 204502.84 |  | actual | historical collections as of date |
| 2025-11 | 299131.85 |  | actual | historical collections as of date |
| 2025-12 | 292282.47 |  | actual | historical collections as of date |
| 2026-01 |  | 265305.72 | forecast | three-month moving average |
| 2026-02 |  | 285573.35 | forecast | three-month moving average |
| 2026-03 |  | 281053.85 | forecast | three-month moving average |
| 2026-01 |  | 249823.02 | future_scheduled_payment | known future-dated synthetic payment, excluded from actuals |
| 2026-02 |  | 100548.58 | future_scheduled_payment | known future-dated synthetic payment, excluded from actuals |

## Business meaning
Use these baselines as directional planning references only; future-dated payments are labeled separately and not mixed with historical actuals.

## ERP/SAP relevance
Forecast outputs support demand planning, cash collection planning, and management reporting outside core transactional processing.

## Limitations
This is not production-grade forecasting; it excludes events, competitor rates, weather, disputes, and formal multi-season backtesting.
