from ai_query_service import execute_interpreted_query


def test_total_revenue_query():
    result = execute_interpreted_query("What is the total revenue?")

    assert result["intent"] == "TOTAL_REVENUE"
    assert result["data"] is not None
    assert result["data"]["total_revenue"] > 0
