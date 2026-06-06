# tidal/opportunity.py
def annual_value(volume, you, cpc, timing):
    """Recoverable clicks/mo * CPC * 12, scaled by timing. you in [0,1]."""
    recoverable_clicks = volume * (1.0 - you)
    return recoverable_clicks * cpc * 12 * timing

def rank(board, demand, timing):
    rows = []
    for row in board:
        topic = row["topic"]
        d = demand.get(topic)
        if not d:
            continue
        t = timing.get(topic, 1.0)
        value = annual_value(d["volume"], row["you"], d["cpc"], t)
        invisibility = round((1.0 - row["you"]) * 100)
        rows.append({
            "topic": topic,
            "volume": d["volume"],
            "cpc": d["cpc"],
            "you": row["you"],
            "timing": t,
            "annual_value": value,
            "why": f"{d['volume']:,} searches/mo · invisible {invisibility}% · ${d['cpc']:.2f} per click",
        })
    rows.sort(key=lambda r: -r["annual_value"])
    return rows
