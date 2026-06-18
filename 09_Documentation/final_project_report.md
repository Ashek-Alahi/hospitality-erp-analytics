# Final Project Report

## Business problem
Hospitality leadership needs a reliable way to connect revenue generation, cash collection, cost control, procurement performance, and inventory risk. When these views are separated, managers can miss relationships between sales activity, working capital, operating profit, and service readiness.

## Project objective
Build a complete, text-based, GitHub-reviewable MVP that demonstrates SAP S/4HANA-inspired ERP analytics using synthetic/anonymized data only. The project is designed for portfolio and interview discussion, not as a claim of real SAP implementation.

## ERP module coverage
| Area | Coverage in this repository |
| --- | --- |
| FI | Revenue trend, accounts receivable aging, cash collections |
| CO | Cost center budget versus actual, variance, profitability summary |
| SD | Revenue by category, channel, and customer segment |
| MM | Purchase spend, vendor performance, and reorder alerts |
| Analytics | Baseline revenue and cash-flow forecasts with simple error metrics |
| BI | HTML dashboard using regenerated KPI and SVG outputs |

## Data model explanation
The model separates master data from transaction data. `customers_clean.csv` supports sales and invoice analysis through `customer_id`. `vendors_clean.csv` supports procurement analysis through `vendor_id`. `customer_invoices_clean.csv` connects to `customer_payments_clean.csv` through `invoice_id`. Period and date fields support monthly trend reporting across finance, controlling, sales, procurement, inventory, and forecasting outputs.

## KPI interpretation
- **Total net revenue** indicates the top-line sales captured in the synthetic sales data.
- **Open AR balance** indicates customer invoice value not yet covered by recorded payments.
- **Operating profit** compares total revenue with actual operating cost in the controlling data.
- **Purchase spend** shows procurement exposure across vendor purchase records.
- **Reorder alerts** identify stock records where closing quantity is at or below reorder point.

## Management recommendations
1. Use AR aging to prioritize collection follow-up and reduce working-capital pressure.
2. Review unfavorable cost center variances before the next budgeting cycle.
3. Compare channel and segment revenue to guide pricing, promotion, and account focus.
4. Monitor vendor delay and spend together when discussing supplier performance.
5. Treat reorder alerts as operational exceptions requiring purchasing or inventory review.
6. Use baseline forecasts for planning discussion only, and gather more history before production forecasting.

## Project limitations
- The dataset is synthetic/anonymized and intentionally small.
- Forecasting uses simple baseline methods and does not include seasonality, events, pricing, occupancy drivers, or external demand indicators.
- The repository does not include SAP configuration, SAP database tables, ABAP code, a `.pbix` report, or a live database.
- CSV files are suitable for transparent portfolio review but do not replace production data governance or security controls.

## Future improvements
- Add a larger synthetic dataset with multiple properties and seasons.
- Add SQL query examples for each module after importing into SQLite.
- Add more granular hospitality metrics such as occupancy, ADR, RevPAR, food and beverage margin, and labor productivity.
- Add dashboard filters and more accessibility improvements to the HTML dashboard.
- Add data quality scorecards and exception reports.

## Interview positioning
This project can be described as a SAP S/4HANA-inspired hospitality ERP analytics prototype. It demonstrates an accountant's ability to connect FI, CO, SD, and MM business processes with Python automation, SQL-ready data modeling, KPI reporting, and honest analytics documentation using only synthetic/anonymized data.
