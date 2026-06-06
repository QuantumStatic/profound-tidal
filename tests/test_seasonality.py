# tests/test_seasonality.py
import pytest
from tidal import data, seasonality

@pytest.fixture(scope="module")
def records():
    return data.load_primary()

def test_daily_soaa_series_length(records):
    series = seasonality.daily_soaa_series(records, "Pricing")
    assert len(series) == 22                      # 22 dates
    for _, v in series:
        assert 0.0 <= v <= 1.0

def test_slope_sign_synthetic():
    rising = [(0, 0.1), (1, 0.2), (2, 0.3), (3, 0.4)]
    flat = [(0, 0.5), (1, 0.5), (2, 0.5)]
    assert seasonality.slope(rising) > 0
    assert seasonality.slope(flat) == pytest.approx(0.0, abs=1e-9)

def test_volatility_synthetic():
    assert seasonality.volatility([(0, 0.5), (1, 0.5)]) == pytest.approx(0.0, abs=1e-9)
    assert seasonality.volatility([(0, 0.0), (1, 1.0)]) > 0

def test_momentum_all_topics(records):
    m = seasonality.momentum(records)
    assert len(m) == 15
    for topic, info in m.items():
        assert "slope" in info and "volatility" in info
