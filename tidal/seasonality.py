# tidal/seasonality.py
from collections import defaultdict
from statistics import pstdev
from tidal import data, metrics

def daily_soaa_series(records, topic):
    """List of (day_index, soaa) ordered by date, for one topic."""
    by_date = defaultdict(list)
    for r in records:
        if r.get("topic") == topic:
            by_date[r.get("date")].append(r)
    dates = sorted(by_date)
    return [(i, metrics.soaa(by_date[d])) for i, d in enumerate(dates)]

def slope(series):
    """OLS slope of y over x for a list of (x, y)."""
    n = len(series)
    if n < 2:
        return 0.0
    sx = sum(x for x, _ in series)
    sy = sum(y for _, y in series)
    sxx = sum(x * x for x, _ in series)
    sxy = sum(x * y for x, y in series)
    denom = n * sxx - sx * sx
    if denom == 0:
        return 0.0
    return (n * sxy - sx * sy) / denom

def volatility(series):
    ys = [y for _, y in series]
    if len(ys) < 2:
        return 0.0
    return pstdev(ys)

def momentum(records):
    out = {}
    for topic in data.distinct(records, "topic"):
        series = daily_soaa_series(records, topic)
        out[topic] = {"slope": slope(series), "volatility": volatility(series)}
    return out
