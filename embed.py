import chromadb
from sentence_transformers import SentenceTransformer
from config import EMBED_MODEL, CHROMA_COLLECTION, TOP_K

_client = None
_collection = None
_model = None


def _get_collection():
    global _client, _collection
    if _collection is None:
        _client = chromadb.PersistentClient(path="./chroma_db")
        _collection = _client.get_or_create_collection(CHROMA_COLLECTION)
    return _collection


def _get_model():
    global _model
    if _model is None:
        _model = SentenceTransformer(EMBED_MODEL)
    return _model


def build_vector_store(chunks: list[dict]) -> None:
    collection = _get_collection()
    model = _get_model()

    texts = [c["text"] for c in chunks]
    metadatas = [{"source_label": c["source_label"], "source_url": c["source_url"]} for c in chunks]
    ids = [f"chunk_{i}" for i in range(len(chunks))]

    print(f"Embedding {len(chunks)} chunks with {EMBED_MODEL}...")
    embeddings = model.encode(texts, show_progress_bar=True).tolist()

    # Clear existing data so re-runs start fresh
    existing = collection.get()
    if existing["ids"]:
        collection.delete(ids=existing["ids"])

    collection.add(documents=texts, embeddings=embeddings, metadatas=metadatas, ids=ids)
    print(f"Stored {len(chunks)} chunks in ChromaDB collection '{CHROMA_COLLECTION}'")


def retrieve(query: str, k: int = TOP_K) -> list[dict]:
    collection = _get_collection()
    model = _get_model()

    query_embedding = model.encode([query]).tolist()
    results = collection.query(query_embeddings=query_embedding, n_results=k)

    chunks = []
    for text, metadata in zip(results["documents"][0], results["metadatas"][0]):
        chunks.append({
            "text": text,
            "source_label": metadata.get("source_label", ""),
            "source_url": metadata.get("source_url", ""),
        })
    return chunks


if __name__ == "__main__":
    from ingest import load_documents, build_chunks

    docs = load_documents()
    chunks = build_chunks(docs)
    build_vector_store(chunks)

    print("\nTest retrieval — 'which dorm has suite-style bathrooms':")
    results = retrieve("which dorm has suite-style bathrooms")
    for i, r in enumerate(results, 1):
        print(f"  [{i}] ({r['source_label']}) {r['text'][:120]!r}...")
