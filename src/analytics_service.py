from database import get_connection


def get_revenue_by_category():
    connection = get_connection()
    cursor = connection.cursor()

    query = """
        SELECT
            p.category,
            ROUND(SUM(oi.quantity * oi.unit_price)::numeric, 2) AS revenue
        FROM order_items oi
        JOIN products p
            ON oi.product_id = p.product_id
        JOIN orders o
            ON oi.order_id = o.order_id
        WHERE o.order_status <> 'Cancelled'
        GROUP BY p.category
        ORDER BY revenue DESC;
    """

    cursor.execute(query)
    results = cursor.fetchall()

    cursor.close()
    connection.close()

    return results


def get_revenue_by_warehouse():
    connection = get_connection()
    cursor = connection.cursor()

    query = """
        SELECT
            w.warehouse_name,
            ROUND(SUM(oi.quantity * oi.unit_price)::numeric, 2) AS revenue
        FROM order_items oi
        JOIN orders o
            ON oi.order_id = o.order_id
        JOIN warehouses w
            ON o.warehouse_id = w.warehouse_id
        WHERE o.order_status <> 'Cancelled'
        GROUP BY w.warehouse_name
        ORDER BY revenue DESC;
    """

    cursor.execute(query)
    results = cursor.fetchall()

    cursor.close()
    connection.close()

    return results

def get_inventory_risk():
    connection = get_connection()
    cursor = connection.cursor()

    query = """
        SELECT
            p.product_name,
            p.category,
            w.warehouse_name,
            i.stock_quantity,
            i.reorder_level,
            (i.reorder_level - i.stock_quantity) AS shortage
        FROM inventory i
        JOIN products p
            ON i.product_id = p.product_id
        JOIN warehouses w
            ON i.warehouse_id = w.warehouse_id
        WHERE i.stock_quantity <= i.reorder_level
        ORDER BY shortage DESC;
    """

    cursor.execute(query)
    results = cursor.fetchall()

    cursor.close()
    connection.close()

    return results

def get_inventory_risk_summary():
    connection = get_connection()
    cursor = connection.cursor()

    query = """
        SELECT
            COUNT(*) AS products_at_risk,
            COALESCE(SUM(reorder_level - stock_quantity), 0) AS total_shortage,
            COUNT(DISTINCT warehouse_id) AS warehouses_affected
        FROM inventory
        WHERE stock_quantity <= reorder_level;
    """

    cursor.execute(query)
    result = cursor.fetchone()

    cursor.close()
    connection.close()

    return result

def get_revenue_by_segment():
    connection = get_connection()
    cursor = connection.cursor()

    query = """
        SELECT
            c.customer_segment,
            COUNT(DISTINCT o.order_id) AS orders,
            ROUND(SUM(o.total_amount)::numeric, 2) AS revenue,
            ROUND(AVG(o.total_amount)::numeric, 2) AS average_order_value
        FROM orders o
        JOIN customers c
            ON o.customer_id = c.customer_id
        WHERE o.order_status <> 'Cancelled'
        GROUP BY c.customer_segment
        ORDER BY revenue DESC;
    """

    cursor.execute(query)
    results = cursor.fetchall()

    cursor.close()
    connection.close()

    return results

def get_delivery_performance():
    connection = get_connection()
    cursor = connection.cursor()

    query = """
        SELECT
            carrier,
            COUNT(*) AS total_deliveries,
            SUM(
                CASE
                    WHEN actual_delivery > expected_delivery
                    THEN 1
                    ELSE 0
                END
            ) AS delayed_deliveries,
            ROUND(
                (
                    SUM(
                        CASE
                            WHEN actual_delivery > expected_delivery
                            THEN 1
                            ELSE 0
                        END
                    )::numeric / COUNT(*)
                ) * 100,
                2
            ) AS delay_rate,
            ROUND(
                AVG(
                    CASE
                        WHEN actual_delivery > expected_delivery
                        THEN delivery_delay_days
                    END
                )::numeric,
                2
            ) AS average_delay_days
        FROM deliveries
        GROUP BY carrier
        ORDER BY delay_rate DESC;
    """

    cursor.execute(query)
    results = cursor.fetchall()

    cursor.close()
    connection.close()

    return results

def get_payment_performance():
    connection = get_connection()
    cursor = connection.cursor()

    query = """
        SELECT
            payment_method,
            COUNT(*) AS total_payments,
            SUM(
                CASE
                    WHEN payment_status = 'Failed'
                    THEN 1
                    ELSE 0
                END
            ) AS failed_payments,
            ROUND(
                (
                    SUM(
                        CASE
                            WHEN payment_status = 'Failed'
                            THEN 1
                            ELSE 0
                        END
                    )::numeric / COUNT(*)
                ) * 100,
                2
            ) AS failure_rate
        FROM payments
        GROUP BY payment_method
        ORDER BY failure_rate DESC;
    """

    cursor.execute(query)
    results = cursor.fetchall()

    cursor.close()
    connection.close()

    return results

def get_return_analysis():
    connection = get_connection()
    cursor = connection.cursor()

    query = """
        SELECT
            return_reason,
            COUNT(*) AS return_count,
            ROUND(
                COUNT(*)::numeric /
                SUM(COUNT(*)) OVER () * 100,
                2
            ) AS return_percentage
        FROM returns
        GROUP BY return_reason
        ORDER BY return_count DESC;
    """

    cursor.execute(query)
    results = cursor.fetchall()

    cursor.close()
    connection.close()

    return results

def get_daily_revenue():
    connection = get_connection()
    cursor = connection.cursor()

    query = """
        SELECT
            DATE(order_date) AS order_day,
            ROUND(SUM(total_amount)::numeric, 2) AS revenue
        FROM orders
        WHERE order_status <> 'Cancelled'
        GROUP BY DATE(order_date)
        ORDER BY order_day;
    """

    cursor.execute(query)
    results = cursor.fetchall()

    cursor.close()
    connection.close()

    return results

def get_revenue_anomalies():
    connection = get_connection()
    cursor = connection.cursor()

    query = """
        WITH daily_revenue AS (
            SELECT
                DATE(order_date) AS order_day,
                SUM(total_amount) AS revenue
            FROM orders
            WHERE order_status <> 'Cancelled'
              AND DATE(order_date) < (SELECT MAX(DATE(order_date)) FROM orders)
            GROUP BY DATE(order_date)
        ),
        revenue_stats AS (
            SELECT
                order_day,
                revenue,
                AVG(revenue) OVER (
                    ORDER BY order_day
                    ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
                ) AS rolling_avg
            FROM daily_revenue
        )
        SELECT
            order_day,
            ROUND(revenue::numeric, 2) AS revenue,
            ROUND(rolling_avg::numeric, 2) AS rolling_average,
            ROUND(
                ((revenue - rolling_avg) / NULLIF(rolling_avg, 0) * 100)::numeric,
                2
            ) AS deviation_percentage,
            CASE
                WHEN revenue > rolling_avg THEN 'Revenue Spike'
                ELSE 'Revenue Drop'
            END AS anomaly_type
        FROM revenue_stats
        WHERE ABS(
            (revenue - rolling_avg) / NULLIF(rolling_avg, 0) * 100
        ) >= 20
        ORDER BY ABS(
            (revenue - rolling_avg) / NULLIF(rolling_avg, 0) * 100
        ) DESC;
    """

    cursor.execute(query)
    results = cursor.fetchall()

    cursor.close()
    connection.close()

    return results

def get_daily_order_demand():
    connection = get_connection()
    cursor = connection.cursor()

    query = """
        SELECT
            DATE(order_date) AS order_day,
            COUNT(*) AS order_count
        FROM orders
        WHERE order_status <> 'Cancelled'
        GROUP BY DATE(order_date)
        ORDER BY order_day;
    """

    cursor.execute(query)
    results = cursor.fetchall()

    cursor.close()
    connection.close()

    return results
