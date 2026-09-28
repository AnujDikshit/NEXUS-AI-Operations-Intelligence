
from database import get_connection

def get_top_revenue_warehouse():
    connection = get_connection()
    cursor = connection.cursor()

    query = '''
        SELECT
            w.warehouse_name,
            ROUND(SUM(o.total_amount)::numeric, 2) AS revenue
        FROM orders o
        JOIN warehouses w
            ON o.warehouse_id = w.warehouse_id
        WHERE o.order_status <> 'Cancelled'
        GROUP BY w.warehouse_name
        ORDER BY revenue DESC
        LIMIT 1;
    '''

    cursor.execute(query)
    result = cursor.fetchone()

    cursor.close()
    connection.close()

    return result


def get_top_revenue_category():
    connection = get_connection()
    cursor = connection.cursor()

    query = '''
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
        ORDER BY revenue DESC
        LIMIT 1;
    '''

    cursor.execute(query)
    result = cursor.fetchone()

    cursor.close()
    connection.close()

    return result


def get_top_revenue_segment():
    connection = get_connection()
    cursor = connection.cursor()

    query = '''
        SELECT
            c.customer_segment,
            ROUND(SUM(o.total_amount)::numeric, 2) AS revenue
        FROM orders o
        JOIN customers c
            ON o.customer_id = c.customer_id
        WHERE o.order_status <> 'Cancelled'
        GROUP BY c.customer_segment
        ORDER BY revenue DESC
        LIMIT 1;
    '''

    cursor.execute(query)
    result = cursor.fetchone()

    cursor.close()
    connection.close()

    return result


def get_products_requiring_reorder():
    connection = get_connection()
    cursor = connection.cursor()

    query = '''
        SELECT
            COUNT(*) AS products_requiring_reorder
        FROM inventory
        WHERE stock_quantity <= reorder_level;
    '''

    cursor.execute(query)
    result = cursor.fetchone()

    cursor.close()
    connection.close()

    return result


def route_business_query(question):
    question = question.lower().strip()

    if "warehouse" in question and any(word in question for word in ["revenue", "sales", "highest", "top", "best"]):
        result = get_top_revenue_warehouse()
        return {
            "intent": "TOP_REVENUE_WAREHOUSE",
            "data": {
                "name": result[0],
                "revenue": float(result[1])
            }
        }

    if "category" in question and any(word in question for word in ["revenue", "sales", "highest", "top", "best"]):
        result = get_top_revenue_category()
        return {
            "intent": "TOP_REVENUE_CATEGORY",
            "data": {
                "category": result[0],
                "revenue": float(result[1])
            }
        }

    if "segment" in question and any(word in question for word in ["revenue", "sales", "highest", "top", "best"]):
        result = get_top_revenue_segment()
        return {
            "intent": "TOP_REVENUE_SEGMENT",
            "data": {
                "segment": result[0],
                "revenue": float(result[1])
            }
        }

    if "reorder" in question or "restock" in question:
        result = get_products_requiring_reorder()
        return {
            "intent": "PRODUCTS_REQUIRING_REORDER",
            "data": {
                "count": result[0]
            }
        }

    return {
        "intent": "UNKNOWN",
        "data": None
    }


def format_query_response(question):
    response = route_business_query(question)

    intent = response["intent"]
    data = response["data"]

    if intent == "TOP_REVENUE_WAREHOUSE":
        name = data["name"]
        revenue = data["revenue"]
        return f"{name} has the highest revenue, generating ₹{float(revenue):,.2f}."

    if intent == "TOP_REVENUE_CATEGORY":
        category = data["category"]
        revenue = data["revenue"]
        return f"{category} is the highest-revenue category, generating ₹{float(revenue):,.2f}."

    if intent == "TOP_REVENUE_SEGMENT":
        segment = data["segment"]
        revenue = data["revenue"]
        return f"{segment} is the highest-revenue customer segment, generating ₹{float(revenue):,.2f}."

    if intent == "PRODUCTS_REQUIRING_REORDER":
        count = data["count"]
        return f"{count:,} products currently require reorder."

    return "I could not identify that business question."
