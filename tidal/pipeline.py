# tidal/pipeline.py
from tidal import metrics, seasonality, opportunity, supply_chain, content, profound_client

OWN_DOMAIN = "openai.com"

def run_streamed(records, month=6):
    subject, confidence = metrics.detect_subject_brand(records)
    yield {"type": "progress", "stage": "listen", "progress": 0.1,
           "message": f"detected subject brand: {subject}"}

    board = metrics.gap_board(records, subject=subject)
    topics = [r["topic"] for r in board]
    for i, t in enumerate(topics, 1):
        yield {"type": "progress", "stage": "listen", "progress": i / len(topics),
               "message": f"probing topic {i}/{len(topics)}: {t}"}

    ghost = metrics.ghost_mention_stats(records, subject=subject)
    yield {"type": "progress", "stage": "opportunity", "progress": 0.3, "message": "pricing the gaps"}

    mom = seasonality.momentum(records)
    timing = {row["topic"]: seasonality.timing_momentum(row["topic"], month, mom)["factor"]
              for row in board}
    demand = profound_client.all_demand()
    opportunities = opportunity.rank(board, demand, timing)

    hero_topic = opportunities[0]["topic"] if opportunities else board[0]["topic"]
    hero_prompt = hero_keyword = f"best ai for {hero_topic.lower()}"
    yield {"type": "progress", "stage": "place", "progress": 0.6,
           "message": f"tracing sources for {hero_topic}"}

    kings = supply_chain.kingmaker_urls(records, hero_topic, limit=5)
    sources = [{"url": k["url"], "count": k["count"],
                "action": supply_chain.route_action(k["url"], own_domain=OWN_DOMAIN)} for k in kings]

    yield {"type": "progress", "stage": "craft", "progress": 0.85, "message": "drafting the brief"}
    hero_content = content.recommendation(records, hero_topic, subject=subject,
                                          prompt=hero_prompt, keyword=hero_keyword, domain=OWN_DOMAIN)

    live = seasonality.timing_momentum(hero_topic, month, mom)
    result = {
        "subject": subject, "subject_confidence": confidence,
        "gap_board": board, "ghost": ghost, "opportunities": opportunities,
        "radar": {"month": month, "live": live, "forecast": seasonality.seasonal_forecast(month)},
        "hero": {"topic": hero_topic, "sources": sources, "content": hero_content},
    }
    yield {"type": "done", "result": result}

def run(records, month=6):
    result = None
    for event in run_streamed(records, month=month):
        if event["type"] == "done":
            result = event["result"]
    return result
