def interpret_question(question):
    question = question.lower().strip()

    if any(word in question for word in ["total revenue", "overall revenue", "total sales", "overall sales"]):
        return {"intent": "TOTAL_REVENUE"}

    if any(phrase in question for phrase in [
        "why did revenue",
        "why revenue",
        "revenue anomaly",
        "revenue spike",
        "revenue drop"
    ]):
        return {"intent": "LATEST_REVENUE_RCA"}

    if "warehouse" in question and any(word in question for word in ["revenue", "sales", "highest", "top", "best"]):
        return {
            "intent": "TOP_REVENUE_WAREHOUSE"
        }

    if "category" in question and any(word in question for word in ["revenue", "sales", "highest", "top", "best"]):
        return {
            "intent": "TOP_REVENUE_CATEGORY"
        }

    if any(word in question for word in ["segment", "customer segment", "customer group"]) and any(word in question for word in ["revenue", "sales", "highest", "top", "best", "most"]):
        return {
            "intent": "TOP_REVENUE_SEGMENT"
        }

    if any(word in question for word in ["reorder", "restock", "stockout"]):
        return {
            "intent": "PRODUCTS_REQUIRING_REORDER"
        }

    return {
        "intent": "UNKNOWN"
    }


def execute_interpreted_query(question):
    from query_service import (
        get_top_revenue_warehouse,
        get_top_revenue_category,
        get_top_revenue_segment,
        get_products_requiring_reorder,
        get_total_revenue,
        get_latest_revenue_root_cause
    )

    interpretation = interpret_question(question)
    intent = interpretation["intent"]

    if intent == "TOTAL_REVENUE":
        result = get_total_revenue()
        data = {"total_revenue": float(result[0])}

    elif intent == "LATEST_REVENUE_RCA":
        result = get_latest_revenue_root_cause()

        if result:
            data = {
                "issue_date": str(result["issue_date"]),
                "anomaly_type": result["anomaly_type"],
                "actual_revenue": float(result["actual_value"]),
                "baseline_revenue": float(result["baseline_value"]),
                "deviation_percent": float(result["deviation"]),
                "explanation": __import__("root_cause_service").generate_rca_explanation(
                    result["issue_date"]
                )
            }
        else:
            data = None

    elif intent == "TOP_REVENUE_WAREHOUSE":
        result = get_top_revenue_warehouse()
        data = {
            "warehouse": result[0],
            "revenue": float(result[1])
        }

    elif intent == "TOP_REVENUE_CATEGORY":
        result = get_top_revenue_category()
        data = {
            "category": result[0],
            "revenue": float(result[1])
        }

    elif intent == "TOP_REVENUE_SEGMENT":
        result = get_top_revenue_segment()
        data = {
            "segment": result[0],
            "revenue": float(result[1])
        }

    elif intent == "PRODUCTS_REQUIRING_REORDER":
        result = get_products_requiring_reorder()
        data = {
            "products_requiring_reorder": result[0]
        }

    else:
        data = None

    return {
        "question": question,
        "intent": intent,
        "data": data
    }
