# tests/test_pipeline_stream.py
from tidal import data, pipeline

def test_run_streamed_emits_progress_then_done():
    records = data.load_primary()
    events = list(pipeline.run_streamed(records, month=6))
    kinds = [e["type"] for e in events]
    assert "progress" in kinds
    assert kinds[-1] == "done"
    final = events[-1]["result"]
    assert final["subject"] == "OpenAI"
    assert len(final["gap_board"]) == 15

def test_run_delegates_to_streamed():
    records = data.load_primary()
    assert pipeline.run(records, month=6)["subject"] == "OpenAI"
