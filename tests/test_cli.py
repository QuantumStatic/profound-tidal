# tests/test_cli.py
from tidal import data, pipeline, cli

def test_format_report_contains_key_beats():
    result = pipeline.run(data.load_primary(), month=6)
    text = cli.format_report(result)
    assert "OpenAI" in text
    assert "Gap board" in text
    assert "Fix first" in text
    assert "$" in text
