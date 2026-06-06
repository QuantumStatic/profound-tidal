# tidal/pipeline.py
from tidal import metrics, seasonality, opportunity, supply_chain, content, profound_client

OWN_DOMAIN = "openai.com"

def run(records, month=6):
    subject, confidence = metrics.detect_subject_brand(records)
    board = metrics.gap_board(records, subject=subject)
    ghost = metrics.ghost_mention_stats(records, subject=subject)

    mom = seasonality.momentum(records)
    timing = {row["topic"]: seasonality.timing_momentum(row["topic"], month, mom)["factor"]
              for row in board}

    demand = profound_client.all_demand()
    opportunities = opportunity.rank(board, demand, timing)

    hero_topic = opportunities[0]["topic"] if opportunities else board[0]["topic"]
    hero_prompt = f"best ai for {hero_topic.lower()}"
    hero_keyword = f"best ai for {hero_topic.lower()}"

    kings = supply_chain.kingmaker_urls(records, hero_topic, limit=5)
    sources = []
    for k in kings:
        action = supply_chain.route_action(k["url"], own_domain=OWN_DOMAIN)
        sources.append({"url": k["url"], "count": k["count"], "action": action})

    hero_content = content.recommendation(
        records, hero_topic, subject=subject,
        prompt=hero_prompt, keyword=hero_keyword, domain=OWN_DOMAIN)

    live = seasonality.timing_momentum(hero_topic, month, mom)
    radar = {
        "month": month,
        "live": live,
        "forecast": seasonality.seasonal_forecast(month),
    }

    return {
        "subject": subject,
        "subject_confidence": confidence,
        "gap_board": board,
        "ghost": ghost,
        "opportunities": opportunities,
        "radar": radar,
        "hero": {"topic": hero_topic, "sources": sources, "content": hero_content},
    }
