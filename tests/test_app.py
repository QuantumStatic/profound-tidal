# tests/test_app.py
from fastapi.testclient import TestClient
from tidal.app import app

client = TestClient(app)

def test_run_endpoint_returns_chain():
    resp = client.get("/api/run?month=6")
    assert resp.status_code == 200
    body = resp.json()
    assert body["subject"] == "OpenAI"
    assert len(body["gap_board"]) == 15
    assert body["radar"]["live"]["basis"] == "measured"

def test_run_endpoint_projected_month():
    body = client.get("/api/run?month=11").json()
    assert body["radar"]["live"]["basis"] == "modeled"

def test_stream_emits_sse_events_ending_in_done():
    with client.stream("GET", "/api/stream?month=6") as resp:
        assert resp.status_code == 200
        payload = "".join(resp.iter_text())
    assert "event: progress" in payload
    assert "event: done" in payload
    assert "probing topic" in payload
