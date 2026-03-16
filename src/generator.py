"""
generator.py
------------
Sends retrieved chunks as context to Claude and returns
a grounded answer with source citations.
"""

import os
import anthropic
from dotenv import load_dotenv

load_dotenv()

CLAUDE_MODEL  = "claude-sonnet-4-20250514"
MAX_TOKENS    = 1024

SYSTEM_PROMPT = """You are a financial document analyst specialising in UK banking \
and regulatory documents published by the Bank of England, FCA, and PRA.

Answer questions using ONLY the context provided below.
Do not use any knowledge outside of the provided context.
If the answer is not contained in the context, respond with exactly:
"This information is not available in the provided documents."

Always cite the source document and page number for every factual claim.
Format citations as: [Source: filename, Page X]"""


def build_prompt(query: str, chunks: list[dict]) -> str:
    """Construct the user message with retrieved context."""
    context = "CONTEXT:\n\n"
    for i, chunk in enumerate(chunks, 1):
        context += f"[{i}] {chunk['source']}, Page {chunk['page']}\n"
        context += chunk['text'] + "\n\n"
    context += f"QUESTION: {query}"
    return context


def generate_answer(query: str, chunks: list[dict]) -> dict:
    """
    Call Claude with the retrieved context and return the answer.

    Returns:
        {'answer': str, 'sources': list[dict], 'model': str}
    """
    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    response = client.messages.create(
        model=CLAUDE_MODEL,
        max_tokens=MAX_TOKENS,
        system=SYSTEM_PROMPT,
        messages=[
            {"role": "user", "content": build_prompt(query, chunks)}
        ]
    )

    return {
        "answer" : response.content[0].text,
        "sources": [{"source": c["source"], "page": c["page"]} for c in chunks],
        "model"  : CLAUDE_MODEL,
    }


if __name__ == "__main__":
    from retriever import retrieve

    query  = "What are the main risks to UK financial stability in 2024?"
    chunks = retrieve(query, k=5)
    result = generate_answer(query, chunks)

    print(f"\nQuestion: {query}")
    print(f"\nAnswer:\n{result['answer']}")
    print(f"\nSources:")
    for s in result['sources']:
        print(f"  - {s['source']}, page {s['page']}")
