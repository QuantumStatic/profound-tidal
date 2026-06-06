# tidal/content.py
from tidal import supply_chain, metrics, profound_client

def content_dna(records, topic, subject):
    """Recipe derived from the winning cited pages + comparative entities for a topic."""
    top = supply_chain.top_domains(records, topic, limit=5)
    leader, _ = metrics.category_leader(
        [r for r in records if r.get("topic") == topic], subject=subject)
    return {
        "format": "Comparison listicle — \"Best AI for " + topic + " 2026\" with table + TL;DR + FAQ",
        "freshness": "Dated current year; refresh within ~18 months or it stops getting cited",
        "voice": "Third-party / community framing (Reddit, YouTube) — not a product page",
        "must_mention": [leader] if leader else [],
        "target_sources": [d["domain"] for d in top],
    }

def recommendation(records, topic, subject, prompt, keyword, domain):
    dna = content_dna(records, topic, subject)
    brief = profound_client.content_brief(topic=topic, prompt=prompt, keyword=keyword, domain=domain)
    return {"topic": topic, "dna": dna, "brief": brief}
