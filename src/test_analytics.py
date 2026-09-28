from analytics_service import get_revenue_by_category, get_revenue_by_warehouse


def test_revenue_by_category():
    results = get_revenue_by_category()

    assert results
    assert len(results) > 0

    for category, revenue in results:
        assert category
        assert float(revenue) >= 0


def test_revenue_by_warehouse():
    results = get_revenue_by_warehouse()

    assert results
    assert len(results) > 0

    for warehouse, revenue in results:
        assert warehouse
        assert float(revenue) >= 0
