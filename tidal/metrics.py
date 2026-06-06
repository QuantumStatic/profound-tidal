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

def ghost_mention_stats(records, subject):
    """Records flagged not-mentioned but where the subject appears in normalized_mentions."""
    if not records:
        return {"reported_soaa": 0.0, "true_soaa": 0.0, "ghost_count": 0}
    reported = sum(1 for r in records if data.is_mentioned(r))
    ghosts = sum(
        1 for r in records
        if not data.is_mentioned(r) and subject in set(data.tokens(r.get("normalized_mentions")))
    )
    n = len(records)
    return {
        "reported_soaa": reported / n,
        "true_soaa": (reported + ghosts) / n,
        "ghost_count": ghosts,
    }

def _by_topic(records):
    groups = defaultdict(list)
    for r in records:
        if r.get("topic") is not None:
            groups[r["topic"]].append(r)
    return groups

def sentiment_topics(records):
    """Topics that carry sentiment analysis (type contains 'Sentiment')."""
    flagged = set()
    for r in records:
        if "Sentiment" in (r.get("type") or "") and r.get("topic") is not None:
            flagged.add(r["topic"])
    return flagged

def gap_board(records, subject):
    groups = _by_topic(records)
    sentiment = sentiment_topics(records)
    board = []
    for topic, recs in groups.items():
        you = presence_rate(recs, subject)
        leader, leader_rate = category_leader(recs, subject)
        board.append({
            "topic": topic,
            "you": you,
            "soaa": soaa(recs),
            "leader": leader,
            "leader_rate": leader_rate,
            "has_sentiment": topic in sentiment,
        })
    board.sort(key=lambda r: r["you"])
    return board
