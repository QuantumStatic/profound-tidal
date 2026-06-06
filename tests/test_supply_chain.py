# tests/test_supply_chain.py
import pytest
from tidal import data, supply_chain

@pytest.fixture(scope="module")
def records():
    return data.load_primary()

def test_top_domains_for_topic(records):
    ranked = supply_chain.top_domains(records, "Support", limit=10)
    assert len(ranked) <= 10
    assert all("domain" in d and "count" in d for d in ranked)
    counts = [d["count"] for d in ranked]
    assert counts == sorted(counts, reverse=True)

def test_kingmaker_urls(records):
    kings = supply_chain.kingmaker_urls(records, "Support", limit=5)
    assert len(kings) <= 5
    assert all(k["url"].startswith("http") for k in kings)

def test_competitor_favoring_reddit(records):
    fav = supply_chain.competitor_favoring(records, "reddit.com", brands=["OpenAI", "Claude"])
    assert fav["Claude"] == pytest.approx(0.57, abs=0.03)
    assert fav["OpenAI"] == pytest.approx(0.42, abs=0.03)

def test_route_reddit_to_comment():
    a = supply_chain.route_action("https://www.reddit.com/r/x/comments/123/thread", own_domain="openai.com")
    assert a["agent"] == "Draft Reddit Comment for Thread"
    assert a["target_url"].startswith("https://www.reddit.com")

def test_route_publisher_to_outreach():
    a = supply_chain.route_action("https://www.pcmag.com/best-ai", own_domain="openai.com")
    assert a["agent"] == "Draft Outreach Email"

def test_route_own_domain_to_optimize():
    a = supply_chain.route_action("https://openai.com/support", own_domain="openai.com")
    assert a["agent"] == "Content Optimization Suggestions"

def test_route_unsupported_returns_none():
    a = supply_chain.route_action("https://www.youtube.com/watch?v=abc", own_domain="openai.com")
    assert a is None
