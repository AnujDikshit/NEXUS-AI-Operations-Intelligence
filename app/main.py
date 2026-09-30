from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI(
    title="NEXUS API",
    description="AI-Powered Business Operations Intelligence API",
    version="1.0.0"
)


@app.on_event("startup")
def warm_delivery_risk_cache():
    import sys
    sys.path.append("src")

    from delivery_risk_service import get_delivery_risk_predictions
    import ai_query_service

    ai_query_service._delivery_risk_cache = get_delivery_risk_predictions()
    print("Delivery risk cache ready.")




@app.get("/")
def root():
    return {
        "project": "NEXUS",
        "status": "online",
        "version": "1.0.0"
    }


@app.get("/kpis")
def get_kpis():
    import sys
    sys.path.append("src")

    from kpi_service import get_kpi_summary

    result = get_kpi_summary()

    return {
        "total_revenue": float(result[0]),
        "total_orders": int(result[1]),
        "average_order_value": float(result[2]),
        "returned_orders": int(result[3]),
        "return_rate": float(result[4])
    }


class QueryRequest(BaseModel):
    question: str


@app.post("/query")
def query_business(request: QueryRequest):
    import sys
    sys.path.append("src")

    from ai_query_service import execute_interpreted_query

    return execute_interpreted_query(request.question)


@app.get("/recommendations")
def get_recommendations():
    import sys
    sys.path.append("src")

    from recommendation_service import get_inventory_recommendations

    return {
        "total_recommendations": len(get_inventory_recommendations()),
        "recommendations": get_inventory_recommendations()
    }
