from ai_query_service import execute_interpreted_query


def test_total_revenue_query():
    result = execute_interpreted_query("What is the total revenue?")

    assert result["intent"] == "TOTAL_REVENUE"
    assert result["data"] is not None
    assert result["data"]["total_revenue"] > 0


def test_top_revenue_segment_query():
    result = execute_interpreted_query(
        "Which customer segment has the most sales?"
    )

    assert result["intent"] == "TOP_REVENUE_SEGMENT"
    assert result["data"] is not None
    assert result["data"]["segment"]
    assert result["data"]["revenue"] > 0
