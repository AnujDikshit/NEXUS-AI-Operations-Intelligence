from database import get_connection


def get_demand_forecast():
    connection = get_connection()
    cursor = connection.cursor()

    query = """
        WITH daily_demand AS (
            SELECT
                DATE(order_date) AS order_day,
                COUNT(*) AS order_count
            FROM orders
            WHERE order_status <> 'Cancelled'
              AND DATE(order_date) < (SELECT MAX(DATE(order_date)) FROM orders)
            GROUP BY DATE(order_date)
        ),
        demand_stats AS (
            SELECT
                order_day,
                order_count,
                AVG(order_count) OVER (
                    ORDER BY order_day
                    ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
                ) AS moving_average
            FROM daily_demand
        )
        SELECT
            order_day,
            order_count,
            ROUND(moving_average::numeric, 2) AS forecast
        FROM demand_stats
        ORDER BY order_day;
    """

    cursor.execute(query)
    results = cursor.fetchall()

    cursor.close()
    connection.close()

    return results
