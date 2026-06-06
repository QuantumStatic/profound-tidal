# tests/test_metrics.py
import pytest
from tidal import data, metrics

@pytest.fixture(scope="module")
def records():
    return data.load_primary()

def test_overall_soaa(records):
    assert metrics.soaa(records) == pytest.approx(8056 / 20849, abs=1e-6)

def test_soaa_by_topic_bounds(records):
    by_topic = metrics.soaa_by_topic(records)
    assert len(by_topic) == 15
    for v in by_topic.values():
        assert 0.0 <= v <= 1.0

def test_soaa_known_anchors(records):
    by_topic = metrics.soaa_by_topic(records)
    assert by_topic["Support"] == pytest.approx(0.073, abs=0.005)
    assert by_topic["Education"] == pytest.approx(0.077, abs=0.005)
    assert by_topic["API"] == pytest.approx(0.937, abs=0.005)

def test_soaa_by_platform_count(records):
    assert len(metrics.soaa_by_platform(records)) == 7

def test_detect_subject_brand(records):
    brand, confidence = metrics.detect_subject_brand(records)
    assert brand == "OpenAI"
    assert confidence > 0.95

def test_presence_rate(records):
    rate = metrics.presence_rate(records, "OpenAI")
    assert 0.0 <= rate <= 1.0
    assert rate >= metrics.soaa(records) - 1e-9

def test_category_leader_excludes_subject(records):
    leader, rate = metrics.category_leader(records, subject="OpenAI")
    assert leader != "OpenAI"
    assert leader == "Claude"
    assert 0.0 <= rate <= 1.0

def test_ghost_mentions_nonnegative(records):
    g = metrics.ghost_mention_stats(records, subject="OpenAI")
    assert g["reported_soaa"] == pytest.approx(metrics.soaa(records), abs=1e-9)
    assert g["true_soaa"] >= g["reported_soaa"]
    assert g["ghost_count"] >= 0

def test_ghost_mentions_synthetic():
    recs = [
        {"mentioned?": "Yes", "normalized_mentions": "OpenAI, Claude"},
        {"mentioned?": "No",  "normalized_mentions": "OpenAI"},      # ghost
        {"mentioned?": "No",  "normalized_mentions": "Claude"},      # not a ghost
    ]
    g = metrics.ghost_mention_stats(recs, subject="OpenAI")
    assert g["ghost_count"] == 1
    assert g["reported_soaa"] == pytest.approx(1/3)
    assert g["true_soaa"] == pytest.approx(2/3)

def test_gap_board_shape(records):
    board = metrics.gap_board(records, subject="OpenAI")
    assert len(board) == 15
    row = next(r for r in board if r["topic"] == "Support")
    assert row["you"] < row["leader_rate"]          # invisible vs rival
    assert row["leader"] != "OpenAI"
    assert 0.0 <= row["you"] <= 1.0
    # sorted ascending by `you` so the worst gaps come first
    yous = [r["you"] for r in board]
    assert yous == sorted(yous)

def test_sentiment_lens_returns_topics(records):
    flags = metrics.sentiment_topics(records)
    assert isinstance(flags, set)
    assert flags.issubset(set(data.distinct(records, "topic")))
