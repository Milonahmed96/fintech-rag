"""
pipeline.py
-----------
End-to-end pipeline: question -> retrieved chunks -> Claude answer.
Loads the vector store once and reuses it for multiple queries.
"""

from retriever import retrieve
from generator import generate_answer


def answer(query: str, k: int = 5) -> dict:
    """
    Answer a question using the RAG pipeline.

    Args:
        query : natural language question
        k     : number of chunks to retrieve

    Returns:
        {
            'question': str,
            'answer'  : str,
            'sources' : [{'source': str, 'page': int, 'score': float}],
            'model'   : str,
        }
    """
    chunks = retrieve(query, k=k)
    result = generate_answer(query, chunks)

    # Add retrieval scores to sources
    for i, source in enumerate(result['sources']):
        source['score'] = chunks[i]['score']

    return {
        'question': query,
        'answer'  : result['answer'],
        'sources' : result['sources'],
        'model'   : result['model'],
    }


if __name__ == "__main__":
    test_questions = [
        "What was the Bank of England base rate in 2025?",
        "What does the FPC say about mortgage affordability?",
        "What is the weather like in London?",  # should return 'not available'
    ]

    for q in test_questions:
        print(f"\n{'='*60}")
        print(f"Q: {q}")
        result = answer(q)
        print(f"\nA: {result['answer']}")
        print(f"\nSources used:")
        for s in result['sources']:
            print(f"  [{s['score']}] {s['source']} p.{s['page']}")