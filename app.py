"""
app.py
------
Streamlit application for the FinTech RAG system.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

import streamlit as st
from pipeline import answer

# ── Page config ──
st.set_page_config(
    page_title="UK Financial Regulation Q&A",
    page_icon="🏦",
    layout="wide"
)

# ── Sidebar ──
with st.sidebar:
    st.title("🏦 FinTech RAG")
    st.markdown("---")
    st.markdown("**Document Collection**")
    st.markdown("""
- Bank of England Financial Stability Reports (2023–2025)
- Bank of England Monetary Policy Reports (2025–2026)
- Bank of England Annual Report 2025
- PRA Annual Report 2024–25
- Climate Financial Disclosure 2025
- APF Annual Report 2025
    """)
    st.markdown("---")
    st.markdown("**System**")
    st.markdown("- Embedding: all-MiniLM-L6-v2")
    st.markdown("- Vector store: ChromaDB (7,504 chunks)")
    st.markdown("- Generator: Claude claude-sonnet-4-20250514")
    st.markdown("- Coverage: 90% nominal")
    st.markdown("---")
    k = st.slider("Chunks to retrieve (k)", min_value=3, max_value=10, value=5)

# ── Main ──
st.title("UK Financial Regulation Q&A")
st.markdown(
    "Ask questions about Bank of England and PRA publications. "
    "Answers are grounded in the source documents with page citations."
)

# Example questions
st.markdown("**Example questions:**")
examples = [
    "What are the main risks to UK financial stability?",
    "What does the FPC say about mortgage affordability?",
    "What is the PRA's approach to stress testing?",
    "What does the Bank of England say about climate risk?",
]
cols = st.columns(2)
for i, ex in enumerate(examples):
    if cols[i % 2].button(ex, use_container_width=True):
        st.session_state['query'] = ex

# Query input
query = st.text_input(
    "Your question:",
    value=st.session_state.get('query', ''),
    placeholder="Ask anything about UK banking regulation...",
)

if st.button("Search", type="primary") and query.strip():
    with st.spinner("Retrieving and generating answer..."):
        result = answer(query.strip(), k=k)

    # Answer
    st.markdown("### Answer")
    st.markdown(result['answer'])

    # Sources
    st.markdown("### Sources Retrieved")
    for i, source in enumerate(result['sources'], 1):
        with st.expander(
            f"[{i}] {source['source']}  —  Page {source['page']}  "
            f"(relevance: {source['score']})"
        ):
            # Find the chunk text
            from retriever import retrieve
            chunks = retrieve(query.strip(), k=k)
            if i <= len(chunks):
                st.markdown(chunks[i-1]['text'])

elif query.strip() == '':
    st.info("Enter a question above to get started.")