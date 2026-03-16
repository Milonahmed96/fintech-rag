"""
chunking.py
-----------
Splits extracted document pages into overlapping chunks
with metadata (source filename, page number, chunk ID).
"""

from langchain_text_splitters import RecursiveCharacterTextSplitter


def chunk_documents(
    documents: list[dict],
    chunk_size: int = 500,
    chunk_overlap: int = 100,
) -> list[dict]:
    """
    Split documents into chunks with metadata.

    Returns a list of dicts:
        {
            'text'    : '...',
            'source'  : 'boe_fsr_2023.pdf',
            'page'    : 14,
            'chunk_id': 'boe_fsr_2023_p14_c2'
        }
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=['\n\n', '\n', '. ', ' ', ''],
    )

    all_chunks = []

    for doc in documents:
        filename = doc['filename']
        # Strip .pdf for cleaner IDs
        doc_id = filename.replace('.pdf', '').replace(' ', '_')

        for page in doc['pages']:
            page_num = page['page_num']
            text     = page['text']

            splits = splitter.split_text(text)

            for chunk_idx, chunk_text in enumerate(splits):
                if len(chunk_text.strip()) < 50:
                    continue   # skip tiny fragments
                all_chunks.append({
                    'text'    : chunk_text.strip(),
                    'source'  : filename,
                    'page'    : page_num,
                    'chunk_id': f"{doc_id}_p{page_num}_c{chunk_idx}",
                })

    print(f"Created {len(all_chunks):,} chunks from {len(documents)} documents.")
    return all_chunks


if __name__ == "__main__":
    from ingestion import load_pdfs
    docs   = load_pdfs()
    chunks = chunk_documents(docs)
    print(f"\nSample chunk:")
    print(f"  Source : {chunks[0]['source']}, page {chunks[0]['page']}")
    print(f"  Text   : {chunks[0]['text'][:200]}")
