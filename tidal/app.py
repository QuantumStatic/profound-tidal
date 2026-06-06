# tidal/app.py
from functools import lru_cache
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from tidal import data, pipeline

app = FastAPI(title="Tidal")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

@lru_cache(maxsize=1)
def _records():
    return data.load_primary()

@app.get("/api/run")
def run(month: int = 6):
    return pipeline.run(_records(), month=month)

import json
from fastapi.responses import StreamingResponse

def _sse(event):
    return f"event: {event['type']}\ndata: {json.dumps(event)}\n\n"

@app.get("/api/stream")
def stream(month: int = 6):
    def gen():
        for event in pipeline.run_streamed(_records(), month=month):
            yield _sse(event)
    return StreamingResponse(gen(), media_type="text/event-stream")
