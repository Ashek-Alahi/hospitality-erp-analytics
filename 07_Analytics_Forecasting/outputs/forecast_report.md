# Analytics and Forecasting Report

Synthetic/anonymized SAP S/4HANA-inspired hospitality ERP analytics prototype. This is not a real SAP implementation.

## Key findings
Compared naive, moving average, and linear trend baselines. Best holdout MAPE is 9.74% from linear trend forecast.

## Forecast metrics
| model | holdout_months | mape_pct | mae |
| --- | --- | --- | --- |
| naive forecast | 3 | 14.15 | 90603.48 |
| moving average forecast | 3 | 16.93 | 103537.6 |
| linear trend forecast | 3 | 9.74 | 59202.52 |

## Business meaning
Use the selected baseline as a planning reference only, not an automated commitment. Large variances should trigger review of events, pricing, channel mix, and seasonality.

## ERP/SAP relevance
Forecast outputs can support demand planning, cash planning, and management reporting outside core transactional processing.

## Limitations
This is not production-grade forecasting; it excludes holidays, events, competitor rates, weather, and formal backtesting across many seasons.
