"""
ingestion.py
------------
Loads PDFs from data/documents/, extracts clean text,
and returns a list of document dictionaries ready for chunking.
"""

import os
import pdfplumber


def load_pdfs(documents_dir: str = "data/documents") -> list[dict]:
    """
    Load all PDFs from the documents directory.

    Returns a list of dicts:
        {
            'filename': 'boe_fsr_2023.pdf',
            'pages': [{'page_num': 1, 'text': '...'}, ...]
        }
    """
    documents = []
    pdf_files = [f for f in os.listdir(documents_dir) if f.endswith('.pdf')]
    pdf_files.sort()

    print(f"Loading {len(pdf_files)} PDFs from {documents_dir}...")

    for filename in pdf_files:
        path = os.path.join(documents_dir, filename)
        try:
            pages = []
            with pdfplumber.open(path) as pdf:
                for page_num, page in enumerate(pdf.pages, 1):
                    text = page.extract_text()
                    if text and len(text.strip()) > 50:
                        # Clean common PDF artifacts
                        text = _clean_text(text)
                        pages.append({'page_num': page_num, 'text': text})

            if pages:
                documents.append({'filename': filename, 'pages': pages})
                total_chars = sum(len(p['text']) for p in pages)
                print(f"  OK  {filename} — {len(pages)} pages, {total_chars:,} chars")
            else:
                print(f"  SKIP {filename} — no extractable text")

        except Exception as e:
            print(f"  ERROR {filename} — {e}")

    print(f"\nLoaded {len(documents)} documents successfully.")
    return documents


def _clean_text(text: str) -> str:
    """Remove common PDF extraction artifacts."""
    import re
    # Remove excessive whitespace
    text = re.sub(r'\n{3,}', '\n\n', text)
    text = re.sub(r' {2,}', ' ', text)
    # Remove page numbers standing alone on a line
    text = re.sub(r'^\s*\d+\s*$', '', text, flags=re.MULTILINE)
    return text.strip()


if __name__ == "__main__":
    docs = load_pdfs()
    total_pages = sum(len(d['pages']) for d in docs)
    print(f"\nTotal pages extracted: {total_pages}")