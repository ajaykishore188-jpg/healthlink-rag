from functools import lru_cache

from fastapi import FastAPI, HTTPException

from app.chunking import chunk_pages
from app.ingest import load_pdf
from app.search import build_index, search
from app.rag import answer_question 
from google.genai import errors

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
@app.get("/ask")
def ask(q: str):
    chunks, vectors = get_index()
    try:
        return answer_question(q, chunks, vectors)
    except errors.ServerError:
        raise HTTPException(
            status_code=503,
            detail="The AI model is busy right now. Please try again in a minute.",
        )