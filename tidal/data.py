# tidal/data.py
import json
from urllib.parse import urlparse
from tidal import config

def load_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)

_primary_cache: list | None = None

def load_primary():
    global _primary_cache
    if _primary_cache is None:
        _primary_cache = load_json(config.PRIMARY_DATA)
    return _primary_cache

def distinct(records, key):
    return sorted({r.get(key) for r in records if r.get(key) is not None})

def tokens(comma_str):
    if not comma_str:
        return []
    return [t.strip() for t in comma_str.split(",") if t.strip()]

def _norm_host(url):
    if not url or not isinstance(url, str):
        return None
    try:
        host = urlparse(url).netloc.lower()
        if host.startswith("www."):
            host = host[4:]
        return host or None
    except Exception:
        return None

def citation_domains(record):
    domains = set()
    for i in range(1, config.NUM_CITATION_COLS + 1):
        url = record.get(f"citation_{i}") or ""
        if url:
            host = _norm_host(url)
            if host:
                domains.add(host)
    return domains

def is_mentioned(record):
    return record.get("mentioned?") == "Yes"
