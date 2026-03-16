import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))


def test_clean_text_removes_extra_whitespace():
    from ingestion import _clean_text
    text = "hello   world\n\n\n\ntest"
    result = _clean_text(text)
    assert "   " not in result
    assert "\n\n\n" not in result


def test_chunk_documents_returns_list():
    from chunking import chunk_documents
    fake_docs = [
        {
            'filename': 'test.pdf',
            'pages': [
                {'page_num': 1, 'text': 'The Bank of England monitors financial stability. ' * 20}
            ]
        }
    ]
    chunks = chunk_documents(fake_docs, chunk_size=100, chunk_overlap=20)
    assert isinstance(chunks, list)
    assert len(chunks) > 0
    assert 'text' in chunks[0]
    assert 'source' in chunks[0]
    assert 'page' in chunks[0]
    assert 'chunk_id' in chunks[0]


def test_chunk_metadata_correct():
    from chunking import chunk_documents
    fake_docs = [
        {
            'filename': 'boe_test.pdf',
            'pages': [
                {'page_num': 5, 'text': 'Financial stability is a core objective. ' * 20}
            ]
        }
    ]
    chunks = chunk_documents(fake_docs, chunk_size=100, chunk_overlap=20)
    assert chunks[0]['source'] == 'boe_test.pdf'
    assert chunks[0]['page'] == 5


def test_build_prompt_contains_query():
    from generator import build_prompt
    chunks = [
        {'text': 'The base rate is 5.25%.', 'source': 'test.pdf', 'page': 3}
    ]
    prompt = build_prompt("What is the base rate?", chunks)
    assert "What is the base rate?" in prompt
    assert "test.pdf" in prompt
    assert "5.25%" in prompt


def test_build_prompt_contains_source():
    from generator import build_prompt
    chunks = [
        {'text': 'Inflation target is 2%.', 'source': 'mpr_2025.pdf', 'page': 10}
    ]
    prompt = build_prompt("What is the inflation target?", chunks)
    assert "mpr_2025.pdf" in prompt
    assert "Page 10" in prompt