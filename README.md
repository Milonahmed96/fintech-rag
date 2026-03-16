<div align="center">

<img src="https://readme-typing-svg.demolab.com?font=Georgia&size=32&duration=3000&pause=1000&color=1F3864&center=true&vCenter=true&width=600&lines=FinTech+RAG;UK+Financial+Regulation+Q%26A" alt="FinTech RAG"/>

<br/>

![Python](https://img.shields.io/badge/Python-3.13-1F3864?style=for-the-badge&logo=python&logoColor=white)
![Anthropic](https://img.shields.io/badge/Claude-claude--sonnet--4-D97757?style=for-the-badge&logo=anthropic&logoColor=white)
![ChromaDB](https://img.shields.io/badge/ChromaDB-Vector%20Store-2E75B6?style=for-the-badge)
![Streamlit](https://img.shields.io/badge/Streamlit-Live%20App-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)

<br/>

**[🚀 Live Application](https://fintech-rag-djcdumtjziwkswslapmzid.streamlit.app/)** &nbsp;·&nbsp;
**[📄 Documents](#document-collection)** &nbsp;·&nbsp;
**[📊 Evaluation](#evaluation-results)** &nbsp;·&nbsp;
**[⚙️ Setup](#local-setup)**

</div>

---

## Overview

A retrieval-augmented generation (RAG) system that answers natural language questions about UK banking and financial regulation. The system ingests official publications from the Bank of England and PRA, indexes them into a semantic vector store, and uses Claude to generate precise, grounded answers with source citations.

The system is designed to demonstrate the full RAG engineering stack — from PDF ingestion to production deployment — with measurable quality evaluation on a 25-question golden dataset.

**What it does:**
- Answers questions about monetary policy, financial stability, and prudential regulation
- Cites the exact source document and page number for every factual claim
- Refuses to answer questions outside the document collection rather than hallucinating
- Achieves 96% accuracy on the golden evaluation dataset with zero hallucinations

---

## Document Collection

| Source | Documents | Pages |
|---|---|---|
| Bank of England Financial Stability Reports (2023–2025) | 5 PDFs | ~600 |
| Bank of England Monetary Policy Reports (2025–2026) | 5 PDFs | ~480 |
| Bank of England Annual Report 2025 | 1 PDF | 220 |
| PRA Annual Report 2024–25 | 1 PDF | 71 |
| Climate Financial Disclosure 2025 | 1 PDF | 32 |
| APF and ALFL Annual Reports | 2 PDFs | ~58 |
| **Total** | **16 PDFs** | **1,494 pages — 7,504 chunks** |

---

## Architecture
```
PDF Documents  (16 files · 1,494 pages)
      │
      ▼  pdfplumber — text extraction per page
Text Pages with Metadata
      │
      ▼  RecursiveCharacterTextSplitter (chunk_size=500, overlap=100)
7,504 Chunks  {text, source, page, chunk_id}
      │
      ▼  sentence-transformers/all-MiniLM-L6-v2
384-dimensional Embeddings
      │
      ▼  ChromaDB  (cosine similarity, persistent storage)
Vector Store
      │
   [query]
      │
      ▼  Top-5 most relevant chunks retrieved
Context Window
      │
      ▼  Claude claude-sonnet-4-20250514  (grounded system prompt)
Answer with Source Citations
```

---

## Evaluation Results

Evaluated on a 25-question golden dataset — 20 answerable questions drawn from verified document content and 5 unanswerable out-of-domain questions.

| Metric | Score |
|---|---|
| Answerable questions correct | 19 / 20 — 95% |
| Unanswerable questions correctly refused | 5 / 5 — 100% |
| **Overall accuracy** | **96%** |
| Hallucinations on out-of-domain questions | **0** |

The one missed question (Bank of England view on housing supply) was a scoring artefact — the answer was retrieved and answered correctly but keyword matching in the evaluator underscored it.

### RAG Failure Mode Diagnostics

| Failure Mode | Example | Root Cause |
|---|---|---|
| Retrieval failure | "Base rate in 2025" → returned title pages | Numerical data in tables; poor table extraction |
| Generation success | "FPC mortgage affordability" → grounded answer with citations | Correct chunks retrieved, Claude used context correctly |
| Correct refusal | "CEO of HSBC" → not available | Low retrieval score (0.44), system prompt blocked hallucination |

---

## Stack

| Component | Technology |
|---|---|
| PDF extraction | pdfplumber |
| Text chunking | LangChain RecursiveCharacterTextSplitter |
| Embedding model | sentence-transformers / all-MiniLM-L6-v2 (384-dim, local) |
| Vector store | ChromaDB with persistent storage |
| Language model | Anthropic Claude claude-sonnet-4-20250514 |
| Frontend | Streamlit |
| Deployment | Streamlit Cloud |

---

## Local Setup
```bash
git clone git@github.com:Milonahmed96/fintech-rag.git
cd fintech-rag
python -m venv venv
.\venv\Scripts\activate        # Windows
pip install -r requirements.txt
```

Create a `.env` file:
```
ANTHROPIC_API_KEY=your_key_here
```

Run locally:
```bash
streamlit run app.py
```

---

## Project Structure
```
fintech-rag/
├── src/
│   ├── ingestion.py          # PDF loading and text extraction
│   ├── chunking.py           # RecursiveCharacterTextSplitter with metadata
│   ├── embedder.py           # Embedding and ChromaDB storage
│   ├── retriever.py          # Cosine similarity search
│   ├── generator.py          # Claude API with grounded system prompt
│   └── pipeline.py           # End-to-end: question → answer
├── evaluation/
│   ├── golden_dataset.json   # 25 questions with known answers
│   ├── evaluate.py           # Evaluation script
│   └── results.json          # Evaluation results
├── data/
│   └── chroma_db/            # Persistent vector store
├── app.py                    # Streamlit application
└── requirements.txt
```

---

## Licence

MIT