-- NEXUS Business KPI Analysis
-- 1. Total Revenue

SELECT
    SUM(total_amount) AS total_revenue
FROM orders
WHERE order_status <> 'Cancelled';

-- 2. Total Orders

SELECT
    COUNT(DISTINCT order_id) AS total_orders
FROM orders;

-- 3. Average Order Value

SELECT
    AVG(total_amount) AS average_order_value
FROM orders
WHERE order_status <> 'Cancelled';

-- 4. Return Rate

SELECT
    COUNT(DISTINCT r.order_id) * 100.0
    / COUNT(DISTINCT o.order_id) AS return_rate
FROM orders o
LEFT JOIN returns r
    ON o.order_id = r.order_id
WHERE o.order_status <> 'Cancelled';

-- 5. Revenue by Product Category

SELECT
    p.category,
    SUM(oi.unit_price * oi.quantity) AS revenue
FROM order_items oi
JOIN products p
    ON oi.product_id = p.product_id
JOIN orders o
    ON oi.order_id = o.order_id
WHERE o.order_status <> 'Cancelled'
GROUP BY p.category
ORDER BY revenue DESC;
-- 6. Revenue by Customer Segment

SELECT
    c.customer_segment,
    SUM(o.total_amount) AS revenue
FROM orders o
JOIN customers c
    ON o.customer_id = c.customer_id
WHERE o.order_status <> 'Cancelled'
GROUP BY c.customer_segment
ORDER BY revenue DESC;

-- 7. Revenue by Warehouse

SELECT
    w.warehouse_name,
    w.city,
    SUM(o.total_amount) AS revenue
FROM orders o
JOIN warehouses w
    ON o.warehouse_id = w.warehouse_id
WHERE o.order_status <> 'Cancelled'
GROUP BY
    w.warehouse_name,
    w.city
ORDER BY revenue DESC;

-- 8. Delivery Delay Analysis

SELECT
    carrier,
    COUNT(*) AS total_deliveries,
    SUM(
        CASE
            WHEN delivery_delay_days > 0 THEN 1
            ELSE 0
        END
    ) AS delayed_deliveries,
    AVG(delivery_delay_days) AS average_delay_days
FROM deliveries
GROUP BY carrier
ORDER BY average_delay_days DESC;

-- 9. Inventory Reorder Risk

SELECT
    i.product_id,
    p.product_name,
    p.category,
    i.warehouse_id,
    i.stock_quantity,
    i.reorder_level
FROM inventory i
JOIN products p
    ON i.product_id = p.product_id
WHERE i.stock_quantity <= i.reorder_level
ORDER BY i.stock_quantity ASC;

-- 10. Payment Failure Rate

SELECT
    COUNT(*) AS total_payments,
    SUM(
        CASE
            WHEN payment_status = 'Failed' THEN 1
            ELSE 0
        END
    ) AS failed_payments,
    ROUND(
        SUM(
            CASE
                WHEN payment_status = 'Failed' THEN 1
                ELSE 0
            END
        ) * 100.0 / COUNT(*),
        2
    ) AS failure_rate
FROM payments;