-- SQLite CLI import script. Run from the repository root after creating an empty database yourself:
-- sqlite3 hospitality_erp.db < 02_Data/sql/schema.sql
-- sqlite3 hospitality_erp.db < 02_Data/sql/load_data.sql
-- This repository intentionally does not include or generate .db/.sqlite binary database files.
.mode csv
.headers on
.import 02_Data/processed/calendar_clean.csv calendar
.import 02_Data/processed/customers_clean.csv customers
.import 02_Data/processed/vendors_clean.csv vendors
.import 02_Data/processed/sales_revenue_clean.csv sales_revenue
.import 02_Data/processed/customer_invoices_clean.csv customer_invoices
.import 02_Data/processed/customer_payments_clean.csv customer_payments
.import 02_Data/processed/cost_center_budget_actual_clean.csv cost_center_budget_actual
.import 02_Data/processed/procurement_vendor_clean.csv procurement_vendor
.import 02_Data/processed/inventory_movements_clean.csv inventory_movements
