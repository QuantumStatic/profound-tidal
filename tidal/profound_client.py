# tidal/profound_client.py
"""Single seam for all Profound access. Part 1: deterministic stubs + table parser.
   Part 3 replaces the bodies of demand_for_topic / content_brief / run_action with
   live MCP calls behind cache.py, WITHOUT changing these signatures."""
import re

def _to_int(s):
    return int(re.sub(r"[^0-9]", "", s) or 0)

def _to_float(s):
    return float(re.sub(r"[^0-9.]", "", s) or 0)

def parse_keyword_table(markdown):
    """Parse the AEO+SEO 'Secondary Keyword' table -> list of dicts."""
    rows = []
    for line in markdown.splitlines():
        line = line.strip()
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) < 4:
            continue
        if cells[0].lower() == "keyword" or set(cells[0]) <= {"-", ":"}:
            continue  # header or separator
        rows.append({
            "keyword": cells[0],
            "volume": _to_int(cells[1]),
            "difficulty": _to_int(cells[2]),
            "cpc": _to_float(cells[3]),
        })
    return rows

# --- stubbed demand (Part 3: live AEO+SEO agent, cached) ---
_STUB_DEMAND = {
    "Support":    {"volume": 12100, "cpc": 23.54},
    "Education":  {"volume": 9900,  "cpc": 8.10},
    "Coding":     {"volume": 12100, "cpc": 23.54},
    "API":        {"volume": 5400,  "cpc": 15.00},
    "Pricing":    {"volume": 8100,  "cpc": 19.80},
    "Enterprise": {"volume": 6600,  "cpc": 21.40},
    "Translation":{"volume": 7300,  "cpc": 4.20},
    "Vision":     {"volume": 5000,  "cpc": 6.50},
    "Writing":    {"volume": 9900,  "cpc": 5.10},
    "Research":   {"volume": 4400,  "cpc": 6.00},
    "Math":       {"volume": 6600,  "cpc": 3.80},
    "Privacy":    {"volume": 3600,  "cpc": 9.20},
    "Safety":     {"volume": 2900,  "cpc": 7.40},
    "Reasoning":  {"volume": 4800,  "cpc": 11.00},
    "Speed":      {"volume": 3300,  "cpc": 8.00},
}

def demand_for_topic(topic):
    return _STUB_DEMAND.get(topic, {"volume": 1000, "cpc": 5.0})

def all_demand():
    return dict(_STUB_DEMAND)

def content_brief(topic, prompt, keyword, domain):
    return (f"# Content Brief — {topic}\n\n"
            f"**Target prompt:** {prompt}\n**Primary keyword:** {keyword}\n**Domain:** {domain}\n\n"
            f"Working title: The Best AI for {topic} in 2026 (Tested)\n"
            f"- Lead with a comparison table; include yourself in the top 3\n"
            f"- Answer the top People-Also-Ask questions verbatim\n"
            f"- Place on a high-authority third-party publisher\n")

def run_action(agent, target_url, brand):
    """Stub for the optional 'Run with Profound' actions (Part 3: live)."""
    return f"[stub] {agent} for {brand} targeting {target_url}"
