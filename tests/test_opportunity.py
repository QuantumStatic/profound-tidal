# tests/test_opportunity.py
import pytest
from tidal import opportunity

DEMAND = {
    "Support":   {"volume": 12100, "cpc": 23.54},
    "Education": {"volume": 9900,  "cpc": 8.10},
    "API":       {"volume": 5400,  "cpc": 15.00},
}

BOARD = [
    {"topic": "Support",   "you": 0.07, "leader": "Claude", "leader_rate": 0.43},
    {"topic": "Education", "you": 0.08, "leader": "Gemini", "leader_rate": 0.38},
    {"topic": "API",       "you": 0.94, "leader": "Claude", "leader_rate": 0.54},
]

def test_opportunity_value_formula():
    v = opportunity.annual_value(volume=12100, you=0.07, cpc=23.54, timing=1.0)
    # 12100 * 0.93 * 23.54 * 12
    assert v == pytest.approx(12100 * 0.93 * 23.54 * 12, rel=1e-6)

def test_rank_orders_by_value_desc():
    ranked = opportunity.rank(BOARD, DEMAND, timing={"Support":1.0,"Education":1.0,"API":1.0})
    values = [r["annual_value"] for r in ranked]
    assert values == sorted(values, reverse=True)
    assert ranked[0]["topic"] == "Support"

def test_rank_includes_inspectable_inputs():
    ranked = opportunity.rank(BOARD, DEMAND, timing={"Support":1.0,"Education":1.0,"API":1.0})
    top = ranked[0]
    for key in ("volume", "cpc", "you", "timing", "annual_value", "why"):
        assert key in top

def test_rank_skips_topics_without_demand():
    ranked = opportunity.rank(BOARD, {"Support": DEMAND["Support"]}, timing={"Support":1.0})
    assert [r["topic"] for r in ranked] == ["Support"]

def test_timing_boosts_value():
    base = opportunity.rank(BOARD, DEMAND, timing={"Support":1.0,"Education":1.0,"API":1.0})
    boosted = opportunity.rank(BOARD, DEMAND, timing={"Support":2.0,"Education":1.0,"API":1.0})
    sb = next(r for r in base if r["topic"]=="Support")["annual_value"]
    sx = next(r for r in boosted if r["topic"]=="Support")["annual_value"]
    assert sx == pytest.approx(sb * 2.0, rel=1e-6)
