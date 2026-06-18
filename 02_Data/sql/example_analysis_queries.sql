-- Example SQL analysis queries for the SAP S/4HANA-inspired hospitality ERP analytics prototype.
-- These assume the CSV files were loaded into tables using schema.sql table names.

-- Executive KPI review: occupancy, ADR, RevPAR, revenue, and operating margin.
SELECT
  ROUND(SUM(s.rooms_sold) * 100.0 / (120 * 30 * COUNT(DISTINCT SUBSTR(s.sale_date, 1, 7))), 2) AS occupancy_rate_pct,
  ROUND(SUM(CASE WHEN s.revenue_category = 'Rooms' THEN s.net_revenue ELSE 0 END) / NULLIF(SUM(s.rooms_sold), 0), 2) AS adr,
  ROUND(SUM(CASE WHEN s.revenue_category = 'Rooms' THEN s.net_revenue ELSE 0 END) / (120 * 30 * COUNT(DISTINCT SUBSTR(s.sale_date, 1, 7))), 2) AS revpar,
  ROUND(SUM(s.net_revenue), 2) AS total_net_revenue,
  ROUND((SUM(s.net_revenue) - (SELECT SUM(actual_amount) FROM cost_center_budget_actual)) * 100.0 / SUM(s.net_revenue), 2) AS operating_profit_margin_pct
FROM sales_revenue s;

-- FI: AR aging and collection rate as of 2025-12-31.
WITH paid AS (
  SELECT invoice_id, SUM(payment_amount) AS paid_amount
  FROM customer_payments
  GROUP BY invoice_id
), open_ar AS (
  SELECT
    i.invoice_id,
    i.customer_id,
    JULIANDAY('2025-12-31') - JULIANDAY(i.due_date) AS days_past_due,
    i.invoice_amount - COALESCE(p.paid_amount, 0) AS outstanding_balance
  FROM customer_invoices i
  LEFT JOIN paid p ON i.invoice_id = p.invoice_id
  WHERE i.invoice_amount - COALESCE(p.paid_amount, 0) > 0
)
SELECT
  CASE
    WHEN days_past_due <= 0 THEN 'Current'
    WHEN days_past_due <= 30 THEN '1-30'
    WHEN days_past_due <= 60 THEN '31-60'
    WHEN days_past_due <= 90 THEN '61-90'
    ELSE '90+'
  END AS aging_bucket,
  ROUND(SUM(outstanding_balance), 2) AS outstanding_balance
FROM open_ar
GROUP BY aging_bucket
ORDER BY MIN(days_past_due);

-- FI: collection rate.
SELECT
  ROUND((SELECT SUM(payment_amount) FROM customer_payments) * 100.0 / SUM(invoice_amount), 2) AS collection_rate_pct
FROM customer_invoices;

-- CO: cost center budget variance ranking.
SELECT
  cost_center_id,
  cost_center_name,
  ROUND(SUM(budget_amount), 2) AS budget_amount,
  ROUND(SUM(actual_amount), 2) AS actual_amount,
  ROUND(SUM(actual_amount) - SUM(budget_amount), 2) AS variance,
  ROUND((SUM(actual_amount) - SUM(budget_amount)) * 100.0 / SUM(budget_amount), 2) AS variance_pct
FROM cost_center_budget_actual
GROUP BY cost_center_id, cost_center_name
ORDER BY variance DESC;

-- SD: revenue by channel, segment, and revenue category.
SELECT s.channel, c.segment, s.revenue_category, ROUND(SUM(s.net_revenue), 2) AS net_revenue
FROM sales_revenue s
JOIN customers c ON s.customer_id = c.customer_id
GROUP BY s.channel, c.segment, s.revenue_category
ORDER BY net_revenue DESC;

-- MM: vendor delay performance.
SELECT
  p.vendor_id,
  v.vendor_name,
  ROUND(SUM(p.purchase_amount), 2) AS purchase_amount,
  ROUND(AVG(CASE WHEN JULIANDAY(p.received_date) > JULIANDAY(p.promised_date) THEN JULIANDAY(p.received_date) - JULIANDAY(p.promised_date) ELSE 0 END), 2) AS avg_delay_days,
  ROUND(SUM(CASE WHEN JULIANDAY(p.received_date) > JULIANDAY(p.promised_date) THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS vendor_delay_rate_pct
FROM procurement_vendor p
JOIN vendors v ON p.vendor_id = v.vendor_id
GROUP BY p.vendor_id, v.vendor_name
ORDER BY vendor_delay_rate_pct DESC;

-- MM: reorder risk summary by item and category.
SELECT
  category,
  item_id,
  item_name,
  COUNT(*) AS alert_months,
  MIN(closing_stock) AS lowest_closing_stock,
  MAX(reorder_point) AS reorder_point
FROM inventory_movements
WHERE closing_stock <= reorder_point
GROUP BY category, item_id, item_name
ORDER BY alert_months DESC, lowest_closing_stock ASC;
