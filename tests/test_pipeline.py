# tests/test_pipeline.py
import pytest
from tidal import data, pipeline

@pytest.fixture(scope="module")
def records():
    return data.load_primary()

def test_run_pipeline_full_chain(records):
    result = pipeline.run(records, month=6)
    assert result["subject"] == "OpenAI"
    assert result["subject_confidence"] > 0.95
    assert len(result["gap_board"]) == 15
    assert len(result["opportunities"]) >= 1
    hero = result["hero"]
    assert hero["topic"] in {r["topic"] for r in result["opportunities"]}
    assert "dna" in hero["content"] and "brief" in hero["content"]
    assert "sources" in hero and len(hero["sources"]) >= 1
    assert result["radar"]["live"]["basis"] == "measured"   # month 6 = June
    assert isinstance(result["radar"]["forecast"], list)

def test_run_pipeline_projected_month(records):
    result = pipeline.run(records, month=11)   # November
    assert result["radar"]["live"]["basis"] == "modeled"
    assert all("annual_value" in o for o in result["opportunities"])

def test_guardrails_hold(records):
    result = pipeline.run(records, month=6)
    for row in result["gap_board"]:
        assert 0.0 <= row["you"] <= 1.0
    assert result["ghost"]["true_soaa"] >= result["ghost"]["reported_soaa"]
