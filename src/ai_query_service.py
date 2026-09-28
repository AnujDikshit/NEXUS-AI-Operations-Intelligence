def interpret_question(question):
    question = question.lower().strip()

    if "warehouse" in question and any(word in question for word in ["revenue", "sales", "highest", "top", "best"]):
        return {
            "intent": "TOP_REVENUE_WAREHOUSE"
        }

    if "category" in question and any(word in question for word in ["revenue", "sales", "highest", "top", "best"]):
        return {
            "intent": "TOP_REVENUE_CATEGORY"
        }

    if "segment" in question and any(word in question for word in ["revenue", "sales", "highest", "top", "best"]):
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
        get_products_requiring_reorder
    )

    interpretation = interpret_question(question)
    intent = interpretation["intent"]

    if intent == "TOP_REVENUE_WAREHOUSE":
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
