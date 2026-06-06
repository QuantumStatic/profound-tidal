# tidal/metrics.py
from collections import Counter, defaultdict
from tidal import data

def soaa(records):
    if not records:
        return 0.0
    mentioned = sum(1 for r in records if data.is_mentioned(r))
    return mentioned / len(records)

def _group_soaa(records, key):
    total = defaultdict(int)
    hit = defaultdict(int)
    for r in records:
        k = r.get(key)
        if k is None:
            continue
        total[k] += 1
        if data.is_mentioned(r):
            hit[k] += 1
    return {k: hit[k] / total[k] for k in total}

def soaa_by_topic(records):
    return _group_soaa(records, "topic")

def soaa_by_platform(records):
    return _group_soaa(records, "platform")

def _brand_counter(records):
    """Per-record set of normalized_mentions tokens, counted across records."""
    c = Counter()
    for r in records:
        for tok in set(data.tokens(r.get("normalized_mentions"))):
            c[tok] += 1
    return c

def detect_subject_brand(records):
    """The entity present in ~100% of mentioned records. Returns (brand, confidence)."""
    mentioned = [r for r in records if data.is_mentioned(r)]
    if not mentioned:
        return (None, 0.0)
    c = _brand_counter(mentioned)
    top = c.most_common(1)
    if not top:
        return (None, 0.0)
    brand, count = top[0]
    return (brand, count / len(mentioned))

def presence_rate(records, brand):
    if not records:
        return 0.0
    n = sum(1 for r in records if brand in set(data.tokens(r.get("normalized_mentions"))))
    return n / len(records)

def category_leader(records, subject):
    c = _brand_counter(records)
    ranked = [(b, n) for b, n in c.most_common() if b != subject]
    if not ranked:
        return (None, 0.0)
    brand = ranked[0][0]
    return (brand, presence_rate(records, brand))
