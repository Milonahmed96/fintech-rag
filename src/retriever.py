"""
retriever.py
------------
Queries the ChromaDB vector store and returns the
top-k most relevant chunks for a given question.
Loads embedder and collection once at module level.
"""

from embedder import load_vector_store

# Load once at import time — not on every query
_collection, _embedder = load_vector_store()


def retrieve(query: str, k: int = 5) -> list[dict]:
    """
    Find the top-k most relevant chunks for a query.

    Returns a list of dicts:
        {'text': '...', 'source': 'filename.pdf', 'page': 14, 'score': 0.87}
    """
    query_embedding = _embedder.encode([query]).tolist()

    results = _collection.query(
        query_embeddings=query_embedding,
        n_results=k,
        include=['documents', 'metadatas', 'distances']
    )

    chunks = []
    for i in range(len(results['documents'][0])):
        chunks.append({
            'text'  : results['documents'][0][i],
            'source': results['metadatas'][0][i]['source'],
            'page'  : results['metadatas'][0][i]['page'],
            'score' : round(1 - results['distances'][0][i], 3),
        })

    return chunks


if __name__ == "__main__":
    test_queries = [
        "What is the Bank of England base rate?",
        "What are the main risks to UK financial stability?",
        "What is the FPC's assessment of household debt?",
    ]

    for query in test_queries:
        print(f"\nQuery: {query}")
        print("-" * 60)
        chunks = retrieve(query, k=3)
        for i, chunk in enumerate(chunks, 1):
            print(f"[{i}] Score: {chunk['score']}  |  {chunk['source']} p.{chunk['page']}")
            print(f"    {chunk['text'][:150]}...")