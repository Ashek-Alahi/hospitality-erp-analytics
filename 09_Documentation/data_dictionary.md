# Data Dictionary

All data is synthetic and anonymized for a SAP S/4HANA-inspired hospitality ERP analytics prototype.

| File | Grain | Business use |
| --- | --- | --- |
| `02_Data/processed/sales_revenue_clean.csv` | Sale/category/channel transaction | SD revenue, channel, and category analysis |
| `02_Data/processed/customer_invoices_clean.csv` | Customer invoice | FI AR aging and outstanding balance |
| `02_Data/processed/customer_payments_clean.csv` | Customer payment | FI cash collection analysis |
| `02_Data/processed/cost_center_budget_actual_clean.csv` | Cost center by month | CO budget variance and profitability |
| `02_Data/processed/procurement_vendor_clean.csv` | Purchase order | MM purchase spend and vendor delivery analysis |
| `02_Data/processed/inventory_movements_clean.csv` | Item by month | MM stock movement and reorder-point analysis |
| `02_Data/processed/customers_clean.csv` | Customer master | Customer segment reporting |
| `02_Data/processed/vendors_clean.csv` | Vendor master | Vendor performance reporting |
| `02_Data/processed/calendar_clean.csv` | Date | Period filtering and time-series reporting |
