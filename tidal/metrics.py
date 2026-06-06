# tidal/metrics.py
from collections import defaultdict
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
        total[k] += 1
        if data.is_mentioned(r):
            hit[k] += 1
    return {k: hit[k] / total[k] for k in total}

def soaa_by_topic(records):
    return _group_soaa(records, "topic")

def soaa_by_platform(records):
    return _group_soaa(records, "platform")
