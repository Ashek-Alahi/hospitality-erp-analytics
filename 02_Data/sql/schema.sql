-- SQLite schema for the synthetic SAP S/4HANA-inspired hospitality ERP analytics prototype.
PRAGMA foreign_keys = ON;
CREATE TABLE calendar (date TEXT PRIMARY KEY, year INTEGER, month INTEGER, month_name TEXT, quarter TEXT, day_of_week TEXT, is_weekend TEXT);
CREATE TABLE customers (customer_id TEXT PRIMARY KEY, customer_name TEXT, segment TEXT, region TEXT);
CREATE TABLE vendors (vendor_id TEXT PRIMARY KEY, vendor_name TEXT, category TEXT, on_time_delivery_pct REAL);
CREATE TABLE sales_revenue (sale_id TEXT PRIMARY KEY, sale_date TEXT, customer_id TEXT, channel TEXT, revenue_category TEXT, net_revenue REAL, rooms_sold INTEGER, FOREIGN KEY(customer_id) REFERENCES customers(customer_id));
CREATE TABLE customer_invoices (invoice_id TEXT PRIMARY KEY, customer_id TEXT, invoice_date TEXT, due_date TEXT, invoice_amount REAL, status TEXT, FOREIGN KEY(customer_id) REFERENCES customers(customer_id));
CREATE TABLE customer_payments (payment_id TEXT PRIMARY KEY, invoice_id TEXT, payment_date TEXT, payment_amount REAL, FOREIGN KEY(invoice_id) REFERENCES customer_invoices(invoice_id));
CREATE TABLE cost_center_budget_actual (period TEXT, cost_center_id TEXT, cost_center_name TEXT, budget_amount REAL, actual_amount REAL);
CREATE TABLE procurement_vendor (po_id TEXT PRIMARY KEY, vendor_id TEXT, order_date TEXT, promised_date TEXT, received_date TEXT, category TEXT, purchase_amount REAL, quantity REAL, FOREIGN KEY(vendor_id) REFERENCES vendors(vendor_id));
CREATE TABLE inventory_movements (period TEXT, item_id TEXT, item_name TEXT, category TEXT, opening_stock REAL, received_qty REAL, issued_qty REAL, closing_stock REAL, reorder_point REAL);
