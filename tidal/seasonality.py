# tidal/seasonality.py
from collections import defaultdict
from statistics import pstdev
from tidal import data, metrics, calendar_model

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

def calendar_factor(topic, month):
    """Modeled multiplier for a topic in a given month (1.0 = neutral)."""
    drivers = calendar_model.DRIVERS.get(topic, {})
    if month in drivers:
        return drivers[month][0]
    return 1.0

def seasonal_forecast(month):
    """All topics with a non-neutral driver this month, as plain-language movers."""
    movers = []
    for topic, months in calendar_model.DRIVERS.items():
        if month in months:
            mult, cause = months[month]
            movers.append({
                "topic": topic,
                "direction": "up" if mult >= 1.0 else "down",
                "multiplier": mult,
                "cause": cause,
            })
    movers.sort(key=lambda m: -m["multiplier"])
    return movers

LIVE_MONTH = 6  # June — our real data window

def timing_momentum(topic, month, momentum_map):
    """Blend measured slope (June) with modeled calendar factor (other months)."""
    cal = calendar_factor(topic, month)
    if month == LIVE_MONTH:
        slope_val = momentum_map.get(topic, {}).get("slope", 0.0)
        # scale slope (typically ~+/-0.01/day) into a gentle multiplier
        factor = 1.0 + slope_val * 10.0
        return {"factor": max(0.5, factor), "basis": "measured"}
    return {"factor": cal, "basis": "modeled"}
