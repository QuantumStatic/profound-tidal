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
