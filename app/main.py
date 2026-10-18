from fastapi import FastAPI

app = FastAPI(title="HealthLink RAG")


@app.get("/health")
def health():
    return {"status": "ok"}