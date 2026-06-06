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

from tidal import calendar_model

def test_calendar_has_all_15_topics():
    assert set(calendar_model.DRIVERS.keys()) == {
        "API","Coding","Education","Enterprise","Math","Pricing","Privacy",
        "Reasoning","Research","Safety","Speed","Support","Translation","Vision","Writing",
    }

def test_calendar_factor_default_is_one():
    assert seasonality.calendar_factor("API", 2) == pytest.approx(1.0)

def test_calendar_factor_spike():
    # Pricing spikes in Q4 (Oct=10) per the budget-season driver
    assert seasonality.calendar_factor("Pricing", 10) > 1.0

def test_seasonal_forecast_lists_movers():
    movers = seasonality.seasonal_forecast(11)   # November
    assert any(m["topic"] == "Support" for m in movers)   # holiday e-commerce
    for m in movers:
        assert "cause" in m and "direction" in m

def test_timing_momentum_basis_labels(records):
    m = seasonality.momentum(records)
    live = seasonality.timing_momentum("Coding", 6, m)
    proj = seasonality.timing_momentum("Pricing", 10, m)
    assert live["basis"] == "measured"
    assert proj["basis"] == "modeled"
    assert live["factor"] > 0
    assert proj["factor"] > 1.0     # Pricing spikes in October

def test_timing_momentum_neutral_topic(records):
    m = seasonality.momentum(records)
    t = seasonality.timing_momentum("API", 2, m)   # no Feb driver
    assert t["factor"] == pytest.approx(1.0, abs=0.5)
