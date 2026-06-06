from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
CACHE_DIR = ROOT / "cache"

PRIMARY_DATA = DATA_DIR / "profound_raw_openai_data_with_citations.json"
ANTHROPIC_DATA = DATA_DIR / "profound_raw_data_anthropic.json"
CHATGPT_DATA = DATA_DIR / "profound_raw_data_chatgpt.json"

# Profound IDs (used live in Part 3 only)
ORG_ID = "1680a859-ec50-451a-a781-995de61d9a40"
CATEGORY_ID = "7943f355-67f3-4792-b172-981db56ef33c"

NUM_CITATION_COLS = 56
