from database import get_connection
from ml_forecast_service import get_ml_demand_forecast


def get_forecast_adjusted_reorder():
    connection = get_connection()
    cursor = connection.cursor()

    forecast = get_ml_demand_forecast()

    forecast_avg = sum(
        float(row["predicted_orders"])
        for row in forecast
    ) / len(forecast)

    query = """
        WITH recent_product_demand AS (
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
        ),
        recent_total_orders AS (
            SELECT
                COUNT(*)::numeric / 30 AS avg_daily_orders
            FROM orders
            WHERE order_status <> 'Cancelled'
              AND DATE(order_date) >= (
                  SELECT MAX(DATE(order_date)) - INTERVAL '30 days'
                  FROM orders
              )
              AND DATE(order_date) < (
                  SELECT MAX(DATE(order_date))
                  FROM orders
              )
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
            rto.avg_daily_orders
        FROM inventory i
        JOIN products p
            ON i.product_id = p.product_id
        JOIN warehouses w
            ON i.warehouse_id = w.warehouse_id
        LEFT JOIN recent_product_demand rd
            ON i.product_id = rd.product_id
        CROSS JOIN recent_total_orders rto
        WHERE i.stock_quantity <= i.reorder_level
        ORDER BY i.stock_quantity ASC;
    """

    cursor.execute(query)
    rows = cursor.fetchall()

    cursor.close()
    connection.close()

    recent_avg_orders = float(rows[0][8]) if rows else 0

    if recent_avg_orders > 0:
        forecast_factor = forecast_avg / recent_avg_orders
    else:
        forecast_factor = 1.0

    recommendations = []

    for row in rows:
        (
            product_id,
            product_name,
            category,
            warehouse,
            current_stock,
            reorder_level,
            units_sold_30d,
            avg_daily_demand,
            _
        ) = row

        forecast_adjusted_demand = (
            float(avg_daily_demand) * forecast_factor
        )

        target_stock = max(
            float(reorder_level),
            forecast_adjusted_demand * 30
        )

        reorder_quantity = max(
            0,
            round(target_stock - current_stock)
        )

        recommendations.append({
            "product_id": product_id,
            "product_name": product_name,
            "category": category,
            "warehouse": warehouse,
            "current_stock": current_stock,
            "reorder_level": reorder_level,
            "avg_daily_demand": float(avg_daily_demand),
            "forecast_adjusted_daily_demand": round(
                forecast_adjusted_demand, 2
            ),
            "recommended_reorder_qty": reorder_quantity
        })

    return recommendations
