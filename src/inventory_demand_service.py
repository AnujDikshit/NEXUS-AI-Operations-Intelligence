from database import get_connection


def get_inventory_demand_intelligence():
    connection = get_connection()
    cursor = connection.cursor()

    query = """
        WITH recent_demand AS (
            SELECT
                oi.product_id,
                SUM(oi.quantity) AS units_sold_30d
            FROM order_items oi
            JOIN orders o
                ON oi.order_id = o.order_id
            WHERE o.order_status <> 'Cancelled'
              AND DATE(o.order_date) >= (
                  SELECT MAX(DATE(order_date)) - INTERVAL '30 days'
                  FROM orders
              )
              AND DATE(o.order_date) < (
                  SELECT MAX(DATE(order_date))
                  FROM orders
              )
            GROUP BY oi.product_id
        )
        SELECT
            p.product_id,
            p.product_name,
            p.category,
            w.warehouse_name,
            i.stock_quantity,
            i.reorder_level,
            COALESCE(rd.units_sold_30d, 0) AS units_sold_30d,
            ROUND(
                COALESCE(rd.units_sold_30d, 0)::numeric / 30,
                2
            ) AS avg_daily_demand,
            CASE
                WHEN COALESCE(rd.units_sold_30d, 0) = 0
                    THEN NULL
                ELSE ROUND(
                    i.stock_quantity::numeric /
                    (rd.units_sold_30d::numeric / 30),
                    1
                )
            END AS estimated_stock_days,
            CASE
                WHEN i.stock_quantity <= i.reorder_level
                    THEN 'Critical'
                WHEN COALESCE(rd.units_sold_30d, 0) > 0
                     AND i.stock_quantity / (rd.units_sold_30d::numeric / 30) <= 90
                    THEN 'High Risk'
                WHEN COALESCE(rd.units_sold_30d, 0) > 0
                     AND i.stock_quantity / (rd.units_sold_30d::numeric / 30) <= 180
                    THEN 'Medium Risk'
                ELSE 'Healthy'
            END AS inventory_status
        FROM inventory i
        JOIN products p
            ON i.product_id = p.product_id
        JOIN warehouses w
            ON i.warehouse_id = w.warehouse_id
        LEFT JOIN recent_demand rd
            ON i.product_id = rd.product_id
        ORDER BY
            CASE
                WHEN i.stock_quantity <= i.reorder_level THEN 1
                WHEN COALESCE(rd.units_sold_30d, 0) > 0
                     AND i.stock_quantity / (rd.units_sold_30d::numeric / 30) <= 90 THEN 2
                WHEN COALESCE(rd.units_sold_30d, 0) > 0
                     AND i.stock_quantity / (rd.units_sold_30d::numeric / 30) <= 180 THEN 3
                ELSE 4
            END,
            estimated_stock_days ASC NULLS LAST;
    """

    cursor.execute(query)
    results = cursor.fetchall()

    cursor.close()
    connection.close()

    return results
