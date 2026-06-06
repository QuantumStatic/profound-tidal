# tests/test_data.py
from tidal import data

def test_load_primary_returns_all_records():
    records = data.load_primary()
    assert len(records) == 20849

def test_record_has_expected_fields():
    r = data.load_primary()[0]
    for key in ("date", "platform", "topic", "prompt", "normalized_mentions", "mentioned?"):
        assert key in r

def test_topics_platforms_dates():
    records = data.load_primary()
    assert len(data.distinct(records, "topic")) == 15
    assert len(data.distinct(records, "platform")) == 7
    assert len(data.distinct(records, "date")) == 22

def test_tokens_splits_comma_string():
    assert data.tokens("Reddit, Claude, GPT,") == ["Reddit", "Claude", "GPT"]
    assert data.tokens("") == []
    assert data.tokens(None) == []

def test_citation_domains_parses_and_dedupes_per_record():
    rec = {"citation_1": "https://www.reddit.com/r/x/1", "citation_2": "https://reddit.com/r/y/2"}
    assert data.citation_domains(rec) == {"reddit.com"}

def test_is_mentioned():
    assert data.is_mentioned({"mentioned?": "Yes"}) is True
    assert data.is_mentioned({"mentioned?": "No"}) is False
