from database import get_connection


def get_reorder_recommendations():
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
            GREATEST(
                i.reorder_level,
                CEIL(
                    COALESCE(rd.units_sold_30d, 0)::numeric
                )
            ) AS target_stock,
            GREATEST(
                0,
                GREATEST(
                    i.reorder_level,
                    CEIL(
                        COALESCE(rd.units_sold_30d, 0)::numeric
                    )
                ) - i.stock_quantity
            ) AS recommended_reorder_qty
        FROM inventory i
        JOIN products p
            ON i.product_id = p.product_id
        JOIN warehouses w
            ON i.warehouse_id = w.warehouse_id
        LEFT JOIN recent_demand rd
            ON i.product_id = rd.product_id
        WHERE i.stock_quantity <= i.reorder_level
           OR (
                COALESCE(rd.units_sold_30d, 0) > 0
                AND i.stock_quantity <
                    COALESCE(rd.units_sold_30d, 0)
              )
        ORDER BY recommended_reorder_qty DESC;
    """

    cursor.execute(query)
    results = cursor.fetchall()

    cursor.close()
    connection.close()

    return results
