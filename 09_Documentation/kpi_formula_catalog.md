# KPI Formula Catalog

| KPI name | Formula | Source/output file | ERP/SAP module | Business meaning | Management decision supported | Limitation |
| --- | --- | --- | --- | --- | --- | --- |
| Total net revenue | Sum of `net_revenue` | `05_SD_Module/outputs/revenue_by_category.csv`, `09_Documentation/kpi_summary.csv` | FI/SD | Total recognized sales activity in the synthetic dataset. | Review overall commercial performance. | Excludes tax, cancellations, and real subledger detail. |
| Collection rate | Total payments / total invoices × 100 | `09_Documentation/kpi_summary.csv` | FI | Shows how much invoiced value has converted to cash. | Prioritize credit control and payment follow-up. | Simplified payment clearing. |
| Open AR balance | Invoice amount minus payments | `03_FI_Module/outputs/ar_aging.csv` | FI | Outstanding receivables exposure. | Focus collection activity. | No disputes or credit memos. |
| AR aging bucket exposure | Outstanding balance grouped by due-date age | `03_FI_Module/outputs/ar_aging.csv` | FI | Shows overdue risk by time bucket. | Escalate older receivables. | Uses fixed as-of date. |
| Operating profit | Total net revenue − actual operating cost | `04_CO_Module/outputs/profitability_summary.csv` | CO | Profit after modeled operating costs. | Review profitability. | No depreciation, tax, or allocations. |
| Operating profit margin | Operating profit / total net revenue × 100 | `04_CO_Module/outputs/profitability_summary.csv` | CO | Profitability percentage. | Assess margin health. | Simplified cost model. |
| Cost center variance | Actual amount − budget amount | `04_CO_Module/outputs/cost_center_variance.csv` | CO | Budget over/under performance. | Review department accountability. | No allocation cycles. |
| Cost center variance percentage | Variance / budget amount × 100 | `04_CO_Module/outputs/cost_center_variance.csv` | CO | Relative cost-center variance. | Rank departments for review. | Budget assumptions are synthetic. |
| Occupancy rate | Rooms sold / available room nights × 100 | `05_SD_Module/outputs/hospitality_kpis.csv` | SD | Utilization of available rooms. | Manage demand and pricing. | Uses simplified room availability. |
| ADR | Room revenue / rooms sold | `05_SD_Module/outputs/hospitality_kpis.csv` | SD | Average daily room rate. | Evaluate pricing. | No room-type mix. |
| RevPAR | Room revenue / available room nights | `05_SD_Module/outputs/hospitality_kpis.csv` | SD | Revenue productivity per available room. | Balance occupancy and rate. | Simplified calendar. |
| Revenue by channel | Sum net revenue by channel | `05_SD_Module/outputs/revenue_by_channel.csv` | SD | Channel concentration. | Manage direct/OTA/corporate mix. | No commission modeling. |
| Revenue by customer segment | Sum net revenue by customer segment | `05_SD_Module/outputs/customer_segment_revenue.csv` | SD | Segment contribution. | Adjust sales focus. | Synthetic customer master. |
| Purchase spend | Sum purchase amount | `06_MM_Module/outputs/purchase_spend.csv` | MM | Procurement spend by category. | Review sourcing and budgets. | No invoice matching. |
| Vendor delay rate | Delayed deliveries / total deliveries × 100 | `06_MM_Module/outputs/vendor_performance.csv` | MM | Supplier reliability. | Review vendors and alternatives. | Simplified promised/received dates. |
| Average delay days | Sum delay days / delivery count | `06_MM_Module/outputs/vendor_performance.csv` | MM | Average lateness. | Prioritize supplier action. | Delay causes are not modeled. |
| Reorder alerts | Closing stock <= reorder point | `06_MM_Module/outputs/reorder_alerts.csv` | MM | Stock items needing replenishment review. | Reorder or expedite supply. | No MRP optimization. |
| Inventory risk | Reorder alerts summarized by category | `06_MM_Module/outputs/inventory_risk_summary.csv` | MM | Category-level stock risk. | Protect service levels. | Closing stock only. |
| Naive forecast | Prior period actual | `07_Analytics_Forecasting/outputs/revenue_forecast.csv` | Analytics | Simple baseline forecast. | Planning benchmark. | Not production-grade forecasting. |
| Moving average forecast | Average of recent periods | `07_Analytics_Forecasting/outputs/revenue_forecast.csv` | Analytics | Smooths short-term volatility. | Planning benchmark. | Limited seasonality handling. |
| Linear trend forecast | Starting actual plus fitted trend slope | `07_Analytics_Forecasting/outputs/revenue_forecast.csv` | Analytics | Directional trend baseline. | Compare trend to actuals. | No external drivers. |
| MAPE | Average absolute percentage error | `07_Analytics_Forecasting/outputs/forecast_metrics.csv` | Analytics | Relative forecast error. | Select baseline with caution. | Unstable if actuals are near zero. |
| MAE | Average absolute error | `07_Analytics_Forecasting/outputs/forecast_metrics.csv` | Analytics | Absolute forecast error. | Understand currency-level deviation. | Scale-dependent. |
