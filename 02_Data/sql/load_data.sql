-- SQLite CLI import guidance for the processed CSV files.
-- Run these commands from the repository root after creating an empty SQLite database yourself.
-- Example:
--   sqlite3 hospitality_erp.db < 02_Data/sql/schema.sql
--   sqlite3 hospitality_erp.db < 02_Data/sql/load_data.sql
--
-- Important: this repository intentionally does not include or generate .db/.sqlite files.
--
-- Header handling:
-- SQLite CLI 3.32.0 and newer supports `.import --csv --skip 1`, which skips the CSV header row.
-- If your SQLite CLI does not support `--skip 1`, either upgrade SQLite or manually remove header rows
-- in a temporary copy outside this repository before importing. Do not commit database files.

.mode csv
.import --csv --skip 1 02_Data/processed/calendar_clean.csv calendar
.import --csv --skip 1 02_Data/processed/customers_clean.csv customers
.import --csv --skip 1 02_Data/processed/vendors_clean.csv vendors
.import --csv --skip 1 02_Data/processed/sales_revenue_clean.csv sales_revenue
.import --csv --skip 1 02_Data/processed/customer_invoices_clean.csv customer_invoices
.import --csv --skip 1 02_Data/processed/customer_payments_clean.csv customer_payments
.import --csv --skip 1 02_Data/processed/cost_center_budget_actual_clean.csv cost_center_budget_actual
.import --csv --skip 1 02_Data/processed/procurement_vendor_clean.csv procurement_vendor
.import --csv --skip 1 02_Data/processed/inventory_movements_clean.csv inventory_movements
