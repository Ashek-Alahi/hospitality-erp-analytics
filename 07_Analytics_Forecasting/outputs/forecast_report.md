# Analytics and Forecasting Report

Synthetic/anonymized SAP S/4HANA-inspired hospitality ERP analytics prototype. This is not a real SAP implementation.

## Key findings
Compared naive, moving average, and linear trend revenue baselines. Best holdout MAPE is 9.74% from linear trend forecast. Cash collections use a three-month moving-average baseline for the next three periods.

## Revenue forecast metrics
| model | holdout_months | mape_pct | mae |
| --- | --- | --- | --- |
| naive forecast | 3 | 14.15 | 90603.48 |
| moving average forecast | 3 | 16.93 | 103537.6 |
| linear trend forecast | 3 | 9.74 | 59202.52 |

## Cash collection forecast
| period | actual_cash_collected | forecast_cash_collected | record_type | method |
| --- | --- | --- | --- | --- |
| 2025-12 | 292282.47 |  | actual | historical collections |
| 2026-01 | 249823.02 |  | actual | historical collections |
| 2026-02 | 100548.58 |  | actual | historical collections |
| 2026-03 |  | 214218.02 | forecast | three-month moving average |
| 2026-04 |  | 188196.54 | forecast | three-month moving average |
| 2026-05 |  | 167654.38 | forecast | three-month moving average |

## Business meaning
Use these baselines as directional planning references only. Large variances should trigger review of events, pricing, channel mix, seasonality, payment terms, and AR follow-up.

## ERP/SAP relevance
Forecast outputs can support demand planning, cash collection planning, and management reporting outside core transactional processing.

## Limitations
This is not production-grade forecasting; it excludes holidays, events, competitor rates, weather, payment disputes, and formal backtesting across many seasons.
