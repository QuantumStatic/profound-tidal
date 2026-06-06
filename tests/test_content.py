# tests/test_content.py
import pytest
from tidal import data, content

@pytest.fixture(scope="module")
def records():
    return data.load_primary()

def test_content_dna_shape(records):
    dna = content.content_dna(records, "Support", subject="OpenAI")
    for key in ("format", "freshness", "voice", "must_mention", "target_sources"):
        assert key in dna
    assert isinstance(dna["must_mention"], list)
    assert isinstance(dna["target_sources"], list)

def test_recommendation_bundles_recipe_and_brief(records):
    rec = content.recommendation(records, "Support", subject="OpenAI",
                                 prompt="best ai for support", keyword="best ai for customer support",
                                 domain="openai.com")
    assert "dna" in rec and "brief" in rec
    assert len(rec["brief"]) > 0
