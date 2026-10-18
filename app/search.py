import numpy as np
from fastembed import TextEmbedding

from app.chunking import chunk_pages
from app.ingest import load_pdf

model = TextEmbedding("BAAI/bge-small-en-v1.5")


def build_index(chunks):
    texts = [c["text"] for c in chunks]
    return np.array(list(model.embed(texts)))


def search(query, chunks, vectors, k=3):
    q = np.array(list(model.embed([query])))[0]
    scores = vectors @ q / (np.linalg.norm(vectors, axis=1) * np.linalg.norm(q))
    top = np.argsort(scores)[::-1][:k]
    return [(float(scores[i]), chunks[i]) for i in top]


if __name__ == "__main__":
    pages = load_pdf("data/hypertension.pdf")
    chunks = chunk_pages(pages)
    vectors = build_index(chunks)
    question = "At what blood pressure level should drug treatment start?"
    for score, c in search(question, chunks, vectors):
        print(f"score={score:.3f} | page {c['page']}")
        print(c["text"][:300])
        print("---")