import os
import requests
from bs4 import BeautifulSoup
from config import CHUNK_SIZE, CHUNK_OVERLAP, SOURCE_MAP, SCRAPE_SOURCES

DOCUMENTS_DIR = os.path.join(os.path.dirname(__file__), "documents")

# Maps .txt filenames (without extension) to their source_label in SOURCE_MAP.
# Add an entry here whenever you drop a new .txt file into /documents.
TXT_LABEL_MAP = {
    "reddit_dorms_ranked":  "reddit_dorms_ranked",
    "college_confidential": "college_confidential",
    "roomsurf_ranking":     "roomsurf_ranking",
}


_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
}


def _scrape_url(source_label: str, url: str) -> dict | None:
    try:
        resp = requests.get(url, timeout=15, headers=_HEADERS)
        resp.raise_for_status()
    except requests.RequestException as e:
        print(f"  [warn] could not fetch {url}: {e}")
        return None

    soup = BeautifulSoup(resp.text, "html.parser")
    # Prefer <main> or <article> to skip nav/footer boilerplate
    container = soup.find("main") or soup.find("article") or soup.body
    if container is None:
        return None
    text = container.get_text(separator=" ", strip=True)
    if not text:
        return None
    return {"text": text, "source_label": source_label, "source_url": url}


def _load_txt_files() -> list[dict]:
    docs = []
    if not os.path.isdir(DOCUMENTS_DIR):
        return docs
    for fname in os.listdir(DOCUMENTS_DIR):
        if not fname.endswith(".txt"):
            continue
        stem = fname[:-4]
        label = TXT_LABEL_MAP.get(stem, stem)
        url = SOURCE_MAP.get(label, "")
        path = os.path.join(DOCUMENTS_DIR, fname)
        with open(path, encoding="utf-8") as f:
            text = f.read().strip()
        if text:
            docs.append({"text": text, "source_label": label, "source_url": url})
    return docs


def load_documents() -> list[dict]:
    docs = []
    print("Scraping static UVA housing pages...")
    for label, url in SCRAPE_SOURCES.items():
        print(f"  {label}")
        doc = _scrape_url(label, url)
        if doc:
            docs.append(doc)
    print(f"Loading .txt files from {DOCUMENTS_DIR}...")
    txt_docs = _load_txt_files()
    docs.extend(txt_docs)
    print(f"  {len(txt_docs)} .txt file(s) loaded")
    print(f"Total documents loaded: {len(docs)}")
    return docs


def chunk_text(doc: dict, chunk_size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> list[dict]:
    text = doc["text"]
    label = doc["source_label"]
    url = doc["source_url"]
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end].strip()
        if chunk:
            chunks.append({"text": chunk, "source_label": label, "source_url": url})
        if end >= len(text):
            break
        start = end - overlap
    return chunks


def build_chunks(docs: list[dict]) -> list[dict]:
    all_chunks = []
    for doc in docs:
        all_chunks.extend(chunk_text(doc))
    return all_chunks


if __name__ == "__main__":
    docs = load_documents()
    chunks = build_chunks(docs)
    print(f"\nTotal chunks: {len(chunks)}")
    print("\nSample — first 3 chunks:")
    for c in chunks[:3]:
        print(f"  [{c['source_label']}] {c['text'][:120]!r}...")
