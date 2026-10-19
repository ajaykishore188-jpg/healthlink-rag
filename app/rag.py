from app.llm import ask_llm
from app.search import search

PROMPT = """You are a careful medical-information assistant.
Answer the question using ONLY the context below.
After each claim, cite the page like (page 19).
Keep the document's wording strength: say "recommends" or "suggests" exactly as the document does.
If the context does not contain the answer, say exactly:
"I could not find this in the provided document."

Context:
{context}

Question: {question}
"""


def answer_question(question, chunks, vectors, k=4):
    results = search(question, chunks, vectors, k)
    context = "\n\n".join(
        f"[page {c['page']}] {c['text']}" for _, c in results
    )
    answer = ask_llm(PROMPT.format(context=context, question=question))
    if "could not find this" in answer.lower():
        return {"answer": answer, "source_pages": []}
    sources = sorted({c["page"] for _, c in results})
    return {"answer": answer, "source_pages": sources}