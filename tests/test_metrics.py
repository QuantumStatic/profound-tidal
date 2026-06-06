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
