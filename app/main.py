from functools import lru_cache

from fastapi import FastAPI

from app.chunking import chunk_pages
from app.ingest import load_pdf
from app.search import build_index, search

app = FastAPI(title="HealthLink RAG")


@lru_cache(maxsize=1)
def get_index():
    chunks = chunk_pages(load_pdf("data/hypertension.pdf"))
    return chunks, build_index(chunks)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/search")
def search_endpoint(q: str, k: int = 3):
    chunks, vectors = get_index()
    results = search(q, chunks, vectors, k)
    return [
        {
            "score": round(score, 3),
            "source": c["source"],
            "page": c["page"],
            "text": c["text"],
        }
        for score, c in results
    ]