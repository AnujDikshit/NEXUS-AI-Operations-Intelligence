from analytics_service import get_revenue_anomalies

def get_revenue_root_causes():
    anomalies = get_revenue_anomalies()

    results = []

    for anomaly in anomalies:
        results.append({
            "issue_type": "Revenue Anomaly",
            "issue_date": anomaly[0],
            "metric": "Revenue",
            "actual_value": anomaly[1],
            "baseline_value": anomaly[2],
            "deviation": anomaly[3],
            "anomaly_type": anomaly[4]
        })

    return results
from database import get_connection

def get_payment_driver(issue_date):
    connection = get_connection()
    cursor = connection.cursor()

    query = """
        SELECT
            COUNT(*) AS total_payments,
            COUNT(*) FILTER (WHERE payment_status = 'Failed') AS failed_payments,
            ROUND(
                COUNT(*) FILTER (WHERE payment_status = 'Failed')::numeric
                / NULLIF(COUNT(*), 0) * 100,
                2
            ) AS failure_rate
        FROM payments p
        JOIN orders o
            ON p.order_id = o.order_id
        WHERE DATE(o.order_date) = %s;
    """

    cursor.execute(query, (issue_date,))
    result = cursor.fetchone()

    cursor.close()
    connection.close()

    return result
from database import get_connection

def get_payment_baseline():
    connection = get_connection()
    cursor = connection.cursor()

    query = """
        SELECT
            ROUND(
                COUNT(*) FILTER (WHERE payment_status = 'Failed')::numeric
                / NULLIF(COUNT(*), 0) * 100,
                2
            ) AS baseline_failure_rate
        FROM payments;
    """

    cursor.execute(query)
    result = cursor.fetchone()

    cursor.close()
    connection.close()

    return result
from database import get_connection

def get_order_demand_driver(issue_date):
    connection = get_connection()
    cursor = connection.cursor()

    query = """
        SELECT
            COUNT(*) FILTER (WHERE order_status <> 'Cancelled') AS orders_on_day
        FROM orders
        WHERE DATE(order_date) = %s;
    """

    cursor.execute(query, (issue_date,))
    result = cursor.fetchone()

    cursor.close()
    connection.close()

    return result
from database import get_connection

def get_order_demand_baseline():
    connection = get_connection()
    cursor = connection.cursor()

    query = """
        SELECT
            ROUND(AVG(daily_orders), 2) AS baseline_daily_orders
        FROM (
            SELECT
                DATE(order_date) AS order_day,
                COUNT(*) AS daily_orders
            FROM orders
            WHERE order_status <> 'Cancelled'
            GROUP BY DATE(order_date)
        ) x;
    """

    cursor.execute(query)
    result = cursor.fetchone()

    cursor.close()
    connection.close()

    return result


def get_aov_driver(issue_date):
    connection = get_connection()
    cursor = connection.cursor()

    query = '''
        SELECT
            ROUND(
                AVG(total_amount) FILTER (WHERE order_status <> 'Cancelled'),
                2
            ) AS aov
        FROM orders
        WHERE DATE(order_date) = %s;
    '''

    cursor.execute(query, (issue_date,))
    result = cursor.fetchone()

    cursor.close()
    connection.close()

    return result


def build_revenue_root_cause(issue_date):
    revenue_events = get_revenue_root_causes()

    event = next(
        item for item in revenue_events
        if item["issue_date"] == issue_date
    )

    payment_actual = get_payment_driver(issue_date)[2]
    payment_baseline = get_payment_baseline()[0]

    order_actual = get_order_demand_driver(issue_date)[0]
    order_baseline = get_order_demand_baseline()[0]

    aov_actual = get_aov_driver(issue_date)[0]
    aov_baseline = get_aov_baseline()[0]

    drivers = []
    evidence = []

    order_change = ((order_actual - order_baseline) / order_baseline) * 100
    aov_change = ((aov_actual - aov_baseline) / aov_baseline) * 100
    payment_change = ((payment_actual - payment_baseline) / payment_baseline) * 100

    if order_change > 10:
        drivers.append({
            "driver": "Order Demand",
            "actual": order_actual,
            "baseline": order_baseline,
            "change_percent": round(float(order_change), 2),
            "evidence": "Order volume increased significantly"
        })
    else:
        evidence.append({
            "driver": "Order Demand",
            "status": "Not supporting",
            "change_percent": round(float(order_change), 2)
        })

    if aov_change > 10:
        drivers.append({
            "driver": "Average Order Value",
            "actual": aov_actual,
            "baseline": aov_baseline,
            "change_percent": round(float(aov_change), 2),
            "evidence": "Average order value increased significantly"
        })
    else:
        evidence.append({
            "driver": "Average Order Value",
            "status": "Not supporting",
            "change_percent": round(float(aov_change), 2)
        })

    if payment_change > 10:
        drivers.append({
            "driver": "Payment Failure Rate",
            "actual": payment_actual,
            "baseline": payment_baseline,
            "change_percent": round(float(payment_change), 2),
            "evidence": "Payment failure rate increased significantly"
        })
    else:
        evidence.append({
            "driver": "Payment Failure Rate",
            "status": "Not supporting",
            "change_percent": round(float(payment_change), 2)
        })

    return {
        "issue": event,
        "drivers": drivers,
        "non_supporting_evidence": evidence
    }


def generate_rca_explanation(issue_date):
    result = build_revenue_root_cause(issue_date)

    issue = result["issue"]
    drivers = result["drivers"]
    evidence = result["non_supporting_evidence"]

    explanation = (
        f"Revenue {issue['anomaly_type'].lower()} detected on "
        f"{issue['issue_date']}. "
        f"Revenue was {float(issue['deviation']):.2f}% "
        f"above the baseline."
    )

    if drivers:
        explanation += " Supporting evidence: "
        explanation += "; ".join(
            f"{d['driver']} changed by {d['change_percent']:.2f}%"
            for d in drivers
        ) + "."

    if evidence:
        explanation += " Non-supporting signals: "
        explanation += "; ".join(
            f"{e['driver']} ({e['change_percent']:.2f}%)"
            for e in evidence
        ) + "."

    return explanation

def generate_rca_explanation(issue_date):
    result = build_revenue_root_cause(issue_date)

    issue = result["issue"]
    drivers = result["drivers"]
    evidence = result["non_supporting_evidence"]

    deviation = float(issue["deviation"])

    if deviation >= 0:
        revenue_statement = (
            f"Revenue was {deviation:.2f}% above the baseline."
        )
    else:
        revenue_statement = (
            f"Revenue was {abs(deviation):.2f}% below the baseline."
        )

    explanation = (
        f"{issue['anomaly_type']} detected on "
        f"{issue['issue_date']}. "
        + revenue_statement
    )

    if drivers:
        explanation += " Supporting evidence: "
        explanation += "; ".join(
            f"{d['driver']} changed by {d['change_percent']:+.2f}%"
            for d in drivers
        ) + "."

    if evidence:
        explanation += " Non-supporting signals: "
        explanation += "; ".join(
            f"{e['driver']} ({e['change_percent']:+.2f}%)"
            for e in evidence
            if abs(float(e['change_percent'])) >= 0.01
        )

        if not any(abs(float(e['change_percent'])) >= 0.01 for e in evidence):
            explanation += " No material changes detected."

        explanation += "."

    return explanation


def build_revenue_root_cause(issue_date):
    revenue_events = get_revenue_root_causes()

    event = next(
        item for item in revenue_events
        if item["issue_date"] == issue_date
    )

    payment_actual = get_payment_driver(issue_date)[2]
    payment_baseline = get_payment_baseline()[0]

    order_actual = get_order_demand_driver(issue_date)[0]
    order_baseline = get_order_demand_baseline()[0]

    aov_actual = get_aov_driver(issue_date)[0]
    aov_baseline = get_aov_baseline()[0]

    order_change = ((order_actual - order_baseline) / order_baseline) * 100
    aov_change = ((aov_actual - aov_baseline) / aov_baseline) * 100
    payment_change = ((payment_actual - payment_baseline) / payment_baseline) * 100

    drivers = []
    evidence = []

    is_drop = event["anomaly_type"] == "Revenue Drop"

    if (not is_drop and order_change > 10) or (is_drop and order_change < -10):
        drivers.append({
            "driver": "Order Demand",
            "actual": order_actual,
            "baseline": order_baseline,
            "change_percent": round(float(order_change), 2),
            "evidence": "Order volume changed in a direction consistent with the revenue anomaly"
        })
    else:
        evidence.append({
            "driver": "Order Demand",
            "status": "Not supporting",
            "change_percent": round(float(order_change), 2)
        })

    if (not is_drop and aov_change > 10) or (is_drop and aov_change < -10):
        drivers.append({
            "driver": "Average Order Value",
            "actual": aov_actual,
            "baseline": aov_baseline,
            "change_percent": round(float(aov_change), 2),
            "evidence": "Average order value changed in a direction consistent with the revenue anomaly"
        })
    else:
        evidence.append({
            "driver": "Average Order Value",
            "status": "Not supporting",
            "change_percent": round(float(aov_change), 2)
        })

    if payment_change > 10:
        drivers.append({
            "driver": "Payment Failure Rate",
            "actual": payment_actual,
            "baseline": payment_baseline,
            "change_percent": round(float(payment_change), 2),
            "evidence": "Payment failure rate increased significantly"
        })
    else:
        evidence.append({
            "driver": "Payment Failure Rate",
            "status": "Not supporting",
            "change_percent": round(float(payment_change), 2)
        })

    return {
        "issue": event,
        "drivers": drivers,
        "non_supporting_evidence": evidence
    }

def get_aov_baseline():
    connection = get_connection()
    cursor = connection.cursor()

    query = '''
        SELECT
            ROUND(
                AVG(total_amount) FILTER (WHERE order_status <> 'Cancelled'),
                2
            ) AS baseline_aov
        FROM orders;
    '''

    cursor.execute(query)
    result = cursor.fetchone()

    cursor.close()
    connection.close()

    return result
