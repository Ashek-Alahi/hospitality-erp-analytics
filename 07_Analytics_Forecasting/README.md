# Analytics and Forecasting Module

This module provides baseline planning analytics for revenue and cash collection using simple, explainable methods.

## Analytics covered
- Revenue baseline forecasting with naive, moving average, and linear trend methods
- Cash collection forecasting using actual collections as of 2025-12-31
- Forecast metrics including holdout MAPE and MAE
- Record types: `actual`, `holdout`, `forecast`, and cash-only `future_scheduled_payment`

## Why simple models are used
The goal is interview-defensible analytics, not random advanced ML. Simple baselines are transparent, auditable, and appropriate for a compact synthetic portfolio dataset.

## Outputs generated
- `outputs/revenue_forecast.csv`
- `outputs/forecast_metrics.csv`
- `outputs/cash_collection_forecast.csv`
- `outputs/forecast_report.md`

## Limitations
Synthetic data only; not production-grade forecasting. The model excludes event calendars, competitor pricing, weather, payment disputes, and multi-season validation.
