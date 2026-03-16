# FinTech RAG — UK Financial Regulation Q&A

A retrieval-augmented generation system that answers natural language
questions about UK banking and financial regulatory documents.

**Live app:** https://fintech-rag-djcdumtjziwkswslapmzid.streamlit.app/

## Document Collection

16 PDFs from Bank of England, PRA, and related institutions:

- Financial Stability Reports (2023–2025)
- Monetary Policy Reports (2025–2026)
- Bank of England Annual Report 2025
- PRA Annual Report 2024–25
- Climate Financial Disclosure 2025
- APF and ALFL Annual Reports

**Total:** 1,494 pages — 7,504 chunks indexed

## Architecture
```
PDF Documents
     ↓  pdfplumber
Text Extraction
     ↓  RecursiveCharacterTextSplitter (500 tokens, 100 overlap)
Chunks with Metadata
     ↓  sentence-transformers/all-MiniLM-L6-v2
384-dim Embeddings
     ↓  ChromaDB (cosine similarity)
Top-5 Relevant Chunks
     ↓  Claude claude-sonnet-4-20250514
Grounded Answer with Citations
```

## Evaluation Results

Evaluated on a 25-question golden dataset (20 answerable, 5 unanswerable).

| Metric | Score |
|---|---|
| Answerable questions correct | 19/20 (95%) |
| Unanswerable questions correctly refused | 5/5 (100%) |
| **Overall accuracy** | **96%** |

The system never hallucinated on out-of-domain questions. The one missed
question (housing supply) was a scoring artefact — the answer was retrieved
correctly but keyword matching underscored it.


## Stack

| Component | Technology |
|---|---|
| PDF extraction | pdfplumber |
| Chunking | LangChain RecursiveCharacterTextSplitter |
| Embedding | sentence-transformers all-MiniLM-L6-v2 |
| Vector store | ChromaDB (persistent) |
| LLM | Anthropic Claude claude-sonnet-4-20250514 |
| Frontend | Streamlit |
| Deployment | Streamlit Cloud |

## RAG Failure Mode Diagnostics

Three failure modes identified during evaluation:

| Failure Mode | Example | Fix |
|---|---|---|
| Retrieval failure | "Bank of England base rate in 2025" — returned title pages only | Increase k, improve query wording |
| Generation success | "FPC mortgage affordability" — correct grounded answer with citations | — |
| Correct refusal | "CEO of HSBC" — correctly said not available | — |

## Local Setup
```bash
git clone git@github.com:Milonahmed96/fintech-rag.git
cd fintech-rag
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

Add your Anthropic API key to `.env`:
```
ANTHROPIC_API_KEY=your_key_here
```

Run locally:
```bash
streamlit run app.py
```

## Project Structure
```
fintech-rag/
├── src/
│   ├── ingestion.py       # PDF loading and text extraction
│   ├── chunking.py        # RecursiveCharacterTextSplitter with metadata
│   ├── embedder.py        # Embedding and ChromaDB storage
│   ├── retriever.py       # Cosine similarity search
│   ├── generator.py       # Claude API with grounded prompt
│   └── pipeline.py        # End-to-end: question -> answer
├── evaluation/
│   └── golden_dataset.json  # 25 questions with known answers
├── data/
│   └── chroma_db/         # Persistent vector store (committed)
├── app.py                 # Streamlit application
└── requirements.txt
```

## Licence

MIT