from database import get_connection


def get_inventory_risk_explanations():
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
            ) AS avg_daily_demand
        FROM inventory i
        JOIN products p
            ON i.product_id = p.product_id
        JOIN warehouses w
            ON i.warehouse_id = w.warehouse_id
        LEFT JOIN recent_demand rd
            ON i.product_id = rd.product_id
        WHERE i.stock_quantity <= i.reorder_level
        ORDER BY
            (i.reorder_level - i.stock_quantity) DESC;
    """

    cursor.execute(query)
    rows = cursor.fetchall()

    cursor.close()
    connection.close()

    explanations = []

    for row in rows:
        (
            product_id,
            product_name,
            category,
            warehouse,
            current_stock,
            reorder_level,
            units_sold_30d,
            avg_daily_demand
        ) = row

        reasons = []

        if current_stock <= reorder_level:
            reasons.append("Stock is at or below reorder level")

        if avg_daily_demand > 0:
            stock_days = current_stock / float(avg_daily_demand)

            if stock_days <= 7:
                reasons.append(
                    f"Only {stock_days:.1f} days of estimated stock remaining"
                )
            elif stock_days <= 30:
                reasons.append(
                    f"Estimated stock coverage is {stock_days:.1f} days"
                )

        if units_sold_30d >= 40:
            reasons.append(
                f"High recent demand: {int(units_sold_30d)} units sold in 30 days"
            )
        elif units_sold_30d >= 20:
            reasons.append(
                f"Moderate recent demand: {int(units_sold_30d)} units sold in 30 days"
            )

        explanations.append({
            "product_id": product_id,
            "product_name": product_name,
            "category": category,
            "warehouse": warehouse,
            "current_stock": current_stock,
            "reorder_level": reorder_level,
            "units_sold_30d": units_sold_30d,
            "avg_daily_demand": float(avg_daily_demand),
            "risk_reasons": " | ".join(reasons)
        })

    return explanations
