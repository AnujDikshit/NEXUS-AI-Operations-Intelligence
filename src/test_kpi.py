from kpi_service import get_kpi_summary


def test_kpi_summary():
    kpi = get_kpi_summary()

    assert kpi is not None
    assert len(kpi) == 5
    assert kpi[0] >= 0
    assert kpi[1] >= 0
    assert kpi[2] >= 0
    assert kpi[3] >= 0
    assert 0 <= float(kpi[4]) <= 100
