from app.ingest import load_pdf


def chunk_pages(pages, chunk_size=800, overlap=100):
    chunks = []
    for p in pages:
        text = p["text"].strip()
        start = 0
        while start < len(text):
            piece = text[start:start + chunk_size]
            if piece.strip():
                chunks.append(
                    {"source": p["source"], "page": p["page"], "text": piece}
                )
            start += chunk_size - overlap
    return chunks


if __name__ == "__main__":
    pages = load_pdf("data/hypertension.pdf")
    chunks = chunk_pages(pages)
    print("Total chunks:", len(chunks))
    print(chunks[20])