from pathlib import Path
from pypdf import PdfReader


def load_pdf(path):
    reader = PdfReader(path)
    pages = []
    for number, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""
        pages.append({"source": Path(path).name, "page": number, "text": text})
    return pages


if __name__ == "__main__":
    pages = load_pdf("data/hypertension.pdf")
    print("Total pages:", len(pages))
    print(pages[5]["text"][:500])