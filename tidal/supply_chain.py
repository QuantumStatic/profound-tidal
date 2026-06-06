# tidal/supply_chain.py
from collections import Counter
from tidal import data

def _topic_records(records, topic):
    return [r for r in records if r.get("topic") == topic]

def top_domains(records, topic, limit=10):
    c = Counter()
    for r in _topic_records(records, topic):
        for dom in data.citation_domains(r):
            c[dom] += 1
    return [{"domain": d, "count": n} for d, n in c.most_common(limit)]

def kingmaker_urls(records, topic, limit=5):
    c = Counter()
    for r in _topic_records(records, topic):
        seen = set()
        for i in range(1, 57):
            url = r.get(f"citation_{i}") or ""
            if url and url not in seen:
                seen.add(url)
                c[url] += 1
    return [{"url": u, "count": n} for u, n in c.most_common(limit)]

def competitor_favoring(records, domain, brands):
    """Among records citing `domain`, the share mentioning each brand."""
    citing = [r for r in records if domain in data.citation_domains(r)]
    if not citing:
        return {b: 0.0 for b in brands}
    out = {}
    for b in brands:
        n = sum(1 for r in citing if b in set(data.tokens(r.get("normalized_mentions"))))
        out[b] = n / len(citing)
    return out

_UNSUPPORTED = {"youtube.com", "m.youtube.com", "youtu.be"}

def route_action(url, own_domain):
    """Relevance-gated: return an action dict only on a confident source->agent match."""
    host = data._norm_host(url) or ""
    if not host:
        return None
    if host == own_domain or host.endswith("." + own_domain):
        return {"agent": "Content Optimization Suggestions", "target_url": url, "kind": "optimize"}
    if "reddit.com" in host:
        return {"agent": "Draft Reddit Comment for Thread", "target_url": url, "kind": "reddit"}
    if host in _UNSUPPORTED:
        return None
    # any other third-party publisher article -> outreach
    return {"agent": "Draft Outreach Email", "target_url": url, "kind": "outreach"}
