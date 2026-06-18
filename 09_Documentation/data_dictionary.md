# Data Dictionary

All files use deterministic synthetic/anonymized data for a SAP S/4HANA-inspired hospitality ERP analytics prototype. The project is not a real SAP implementation.

| File name | Column name | Data type | Business meaning | ERP module relevance | Key / relationship notes |
| --- | --- | --- | --- | --- | --- |
| `02_Data/processed/customers_clean.csv` | `customer_id` | Text | Unique synthetic customer identifier | SD, FI | Primary key; joins to `sales_revenue_clean.csv.customer_id` and `customer_invoices_clean.csv.customer_id` |
| `02_Data/processed/customers_clean.csv` | `customer_name` | Text | Synthetic customer display name | SD, FI | Descriptive master-data attribute |
| `02_Data/processed/customers_clean.csv` | `segment` | Text | Customer grouping such as corporate, leisure, or event business | SD | Used for customer segment revenue reporting |
| `02_Data/processed/customers_clean.csv` | `region` | Text | Synthetic customer region | SD | Supports geographic review if extended |
| `02_Data/processed/vendors_clean.csv` | `vendor_id` | Text | Unique synthetic vendor identifier | MM | Primary key; joins to `procurement_vendor_clean.csv.vendor_id` |
| `02_Data/processed/vendors_clean.csv` | `vendor_name` | Text | Synthetic vendor display name | MM | Descriptive vendor master-data attribute |
| `02_Data/processed/vendors_clean.csv` | `category` | Text | Vendor supply category | MM | Supports purchasing category analysis |
| `02_Data/processed/vendors_clean.csv` | `on_time_delivery_pct` | Decimal | Vendor master reference delivery performance percentage | MM | Used as contextual vendor-performance attribute |
| `02_Data/processed/calendar_clean.csv` | `date` | Date | Calendar date in `YYYY-MM-DD` format | Cross-module | Primary calendar key for date filtering |
| `02_Data/processed/calendar_clean.csv` | `year` | Integer | Calendar year | Cross-module | Derived from `date` |
| `02_Data/processed/calendar_clean.csv` | `month` | Integer | Calendar month number | Cross-module | Derived from `date` |
| `02_Data/processed/calendar_clean.csv` | `month_name` | Text | Calendar month name | Cross-module | Reporting label |
| `02_Data/processed/calendar_clean.csv` | `quarter` | Text | Calendar quarter | Cross-module | Reporting period attribute |
| `02_Data/processed/calendar_clean.csv` | `day_of_week` | Text | Day name | Cross-module | Supports weekday/weekend analysis |
| `02_Data/processed/calendar_clean.csv` | `is_weekend` | Boolean text | Weekend flag | Cross-module | Useful for hospitality demand review |
| `02_Data/processed/sales_revenue_clean.csv` | `sale_id` | Text | Unique synthetic sales transaction identifier | SD, FI | Primary transaction key |
| `02_Data/processed/sales_revenue_clean.csv` | `sale_date` | Date | Revenue posting date | SD, FI | Can join to `calendar_clean.csv.date` |
| `02_Data/processed/sales_revenue_clean.csv` | `customer_id` | Text | Customer attached to the sale | SD, FI | Foreign key to `customers_clean.csv.customer_id` |
| `02_Data/processed/sales_revenue_clean.csv` | `channel` | Text | Booking or sales channel | SD | Used for revenue by channel |
| `02_Data/processed/sales_revenue_clean.csv` | `revenue_category` | Text | Revenue type such as rooms, food, or events | SD, FI | Used for category mix and room KPI calculations |
| `02_Data/processed/sales_revenue_clean.csv` | `net_revenue` | Decimal | Net revenue amount | SD, FI | Summed for revenue trend and KPI summary |
| `02_Data/processed/sales_revenue_clean.csv` | `rooms_sold` | Integer | Rooms sold associated with the revenue row | SD | Used for occupancy, ADR, and RevPAR calculations |
| `02_Data/processed/customer_invoices_clean.csv` | `invoice_id` | Text | Unique synthetic customer invoice identifier | FI | Primary invoice key; joins to `customer_payments_clean.csv.invoice_id` |
| `02_Data/processed/customer_invoices_clean.csv` | `customer_id` | Text | Customer billed by the invoice | FI, SD | Foreign key to `customers_clean.csv.customer_id` |
| `02_Data/processed/customer_invoices_clean.csv` | `invoice_date` | Date | Invoice issue date | FI | Supports AR timing analysis |
| `02_Data/processed/customer_invoices_clean.csv` | `due_date` | Date | Payment due date | FI | Used for AR aging buckets |
| `02_Data/processed/customer_invoices_clean.csv` | `invoice_amount` | Decimal | Gross invoice amount | FI | Compared with payments to calculate outstanding balance |
| `02_Data/processed/customer_invoices_clean.csv` | `status` | Text | Synthetic invoice status | FI | Descriptive AR attribute |
| `02_Data/processed/customer_payments_clean.csv` | `payment_id` | Text | Unique synthetic payment identifier | FI | Primary payment key |
| `02_Data/processed/customer_payments_clean.csv` | `invoice_id` | Text | Invoice cleared or partially paid | FI | Foreign key to `customer_invoices_clean.csv.invoice_id` |
| `02_Data/processed/customer_payments_clean.csv` | `payment_date` | Date | Cash receipt date | FI | Used for cash collection history and forecast baseline |
| `02_Data/processed/customer_payments_clean.csv` | `payment_amount` | Decimal | Cash collected amount | FI | Summed for collection rate and monthly collections |
| `02_Data/processed/cost_center_budget_actual_clean.csv` | `period` | Text | Month in `YYYY-MM` format | CO | Cost reporting period |
| `02_Data/processed/cost_center_budget_actual_clean.csv` | `cost_center_id` | Text | Synthetic cost center identifier | CO | Cost center key |
| `02_Data/processed/cost_center_budget_actual_clean.csv` | `cost_center_name` | Text | Cost center description | CO | Reporting label |
| `02_Data/processed/cost_center_budget_actual_clean.csv` | `budget_amount` | Decimal | Monthly budget amount | CO | Compared with actuals for variance |
| `02_Data/processed/cost_center_budget_actual_clean.csv` | `actual_amount` | Decimal | Monthly actual cost amount | CO | Used for operating cost and variance |
| `02_Data/processed/procurement_vendor_clean.csv` | `po_id` | Text | Unique synthetic purchase order identifier | MM | Primary purchasing transaction key |
| `02_Data/processed/procurement_vendor_clean.csv` | `vendor_id` | Text | Vendor on the purchase order | MM | Foreign key to `vendors_clean.csv.vendor_id` |
| `02_Data/processed/procurement_vendor_clean.csv` | `order_date` | Date | Purchase order date | MM | Supports purchasing timeline analysis |
| `02_Data/processed/procurement_vendor_clean.csv` | `promised_date` | Date | Vendor promised receipt date | MM | Compared with receipt date for delay metrics |
| `02_Data/processed/procurement_vendor_clean.csv` | `received_date` | Date | Goods receipt date | MM | Used for delivery delay analysis |
| `02_Data/processed/procurement_vendor_clean.csv` | `category` | Text | Purchasing category | MM | Used for spend by category |
| `02_Data/processed/procurement_vendor_clean.csv` | `purchase_amount` | Decimal | Purchase order value | MM, CO | Summed for purchase spend KPI |
| `02_Data/processed/procurement_vendor_clean.csv` | `quantity` | Integer | Purchased quantity | MM | Operational purchasing measure |
| `02_Data/processed/inventory_movements_clean.csv` | `period` | Text | Month in `YYYY-MM` format | MM | Inventory reporting period |
| `02_Data/processed/inventory_movements_clean.csv` | `item_id` | Text | Synthetic inventory item identifier | MM | Item key within inventory analysis |
| `02_Data/processed/inventory_movements_clean.csv` | `item_name` | Text | Inventory item description | MM | Reporting label |
| `02_Data/processed/inventory_movements_clean.csv` | `category` | Text | Inventory category | MM | Used for inventory risk summary |
| `02_Data/processed/inventory_movements_clean.csv` | `opening_stock` | Integer | Beginning stock balance | MM | Beginning inventory quantity |
| `02_Data/processed/inventory_movements_clean.csv` | `received_qty` | Integer | Quantity received during the period | MM | Inbound stock movement |
| `02_Data/processed/inventory_movements_clean.csv` | `issued_qty` | Integer | Quantity issued or consumed during the period | MM | Outbound stock movement |
| `02_Data/processed/inventory_movements_clean.csv` | `closing_stock` | Integer | Ending stock balance | MM | Compared with reorder point |
| `02_Data/processed/inventory_movements_clean.csv` | `reorder_point` | Integer | Minimum stock threshold | MM | Reorder alert trigger when closing stock is at or below this level |
