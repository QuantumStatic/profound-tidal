# tests/test_profound_client.py
from tidal import profound_client as pc

SAMPLE_TABLE = """
Some preamble.

## Secondary Keywords

| Keyword | Volume | Difficulty | CPC | Intent | SERP features |
|---|---|---|---|---|---|
| best ai for coding | 12,100 | 11 | $23.54 | commercial | AI Overview |
| agentic ai coding tools | 12,100 | 11 | $0.00 | commercial | - |

More text.
"""

def test_parse_secondary_keyword_table():
    rows = pc.parse_keyword_table(SAMPLE_TABLE)
    assert rows[0]["keyword"] == "best ai for coding"
    assert rows[0]["volume"] == 12100
    assert rows[0]["cpc"] == 23.54
    assert rows[1]["cpc"] == 0.0

def test_demand_for_topic_returns_volume_cpc():
    d = pc.demand_for_topic("Coding")
    assert "volume" in d and "cpc" in d
    assert d["volume"] > 0

def test_content_brief_returns_text():
    brief = pc.content_brief(topic="Support", prompt="best ai for support",
                             keyword="best ai for customer support", domain="openai.com")
    assert isinstance(brief, str) and len(brief) > 0
