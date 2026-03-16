"""
embedder.py
-----------
Embeds all chunks using sentence-transformers and stores
them in a persistent ChromaDB vector store.
"""

import os
import chromadb
from sentence_transformers import SentenceTransformer
from chunking import chunk_documents
from ingestion import load_pdfs


CHROMA_PATH  = "data/chroma_db"
COLLECTION   = "fintech_docs"
EMBED_MODEL  = "all-MiniLM-L6-v2"


def build_vector_store(chunks: list[dict]) -> chromadb.Collection:
    """
    Embed all chunks and store in ChromaDB.
    Skips chunks that already exist (safe to re-run).
    """
    os.makedirs(CHROMA_PATH, exist_ok=True)

    print(f"Loading embedding model: {EMBED_MODEL}")
    embedder = SentenceTransformer(EMBED_MODEL)

    client     = chromadb.PersistentClient(path=CHROMA_PATH)
    collection = client.get_or_create_collection(
        name=COLLECTION,
        metadata={"hnsw:space": "cosine"}
    )

    existing = set(collection.get()['ids'])
    new_chunks = [c for c in chunks if c['chunk_id'] not in existing]

    if not new_chunks:
        print(f"Vector store already contains {len(existing)} chunks. Nothing to add.")
        return collection

    print(f"Embedding {len(new_chunks):,} new chunks...")

    # Process in batches to show progress
    batch_size = 256
    for i in range(0, len(new_chunks), batch_size):
        batch = new_chunks[i : i + batch_size]
        texts     = [c['text']     for c in batch]
        ids       = [c['chunk_id'] for c in batch]
        metadatas = [{'source': c['source'], 'page': c['page']} for c in batch]

        embeddings = embedder.encode(texts, show_progress_bar=False).tolist()

        collection.add(
            documents=texts,
            embeddings=embeddings,
            metadatas=metadatas,
            ids=ids,
        )
        print(f"  Embedded {min(i + batch_size, len(new_chunks)):,} / {len(new_chunks):,}")

    print(f"\nVector store ready — {collection.count():,} chunks total.")
    return collection


def load_vector_store() -> tuple[chromadb.Collection, SentenceTransformer]:
    """Load existing vector store and embedder for querying."""
    embedder   = SentenceTransformer(EMBED_MODEL)
    client     = chromadb.PersistentClient(path=CHROMA_PATH)
    collection = client.get_or_create_collection(
        name=COLLECTION,
        metadata={"hnsw:space": "cosine"}
    )
    return collection, embedder


if __name__ == "__main__":
    docs   = load_pdfs()
    chunks = chunk_documents(docs)
    build_vector_store(chunks)
