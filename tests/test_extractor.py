"""Tests for document text extraction (PDF, DOCX, TXT)."""

import os
import pytest
from app.services.extractor import (
    extract_text_from_pdf,
    extract_text_from_docx,
    extract_text_from_txt,
    extract_document_text
)

SAMPLE_RESUMES_DIR = os.path.join(os.path.dirname(__file__), "..", "sample_data", "resumes")


def test_extract_txt():
    txt_path = os.path.join(SAMPLE_RESUMES_DIR, "Alex_Rivera_FullStack_Resume.txt")
    text = extract_document_text("Alex_Rivera_FullStack_Resume.txt", txt_path)
    assert len(text) > 100
    assert "Alex Rivera" in text
    assert "React" in text


def test_extract_docx():
    docx_path = os.path.join(SAMPLE_RESUMES_DIR, "Alex_Rivera_FullStack_Resume.docx")
    assert os.path.exists(docx_path)
    with open(docx_path, "rb") as f:
        content = f.read()
    text = extract_document_text("Alex_Rivera_FullStack_Resume.docx", content)
    assert len(text) > 100
    assert "Alex Rivera" in text
    assert "FastAPI" in text


def test_extract_pdf():
    pdf_path = os.path.join(SAMPLE_RESUMES_DIR, "Dr_Elena_Rostova_AI_NLP_Resume.pdf")
    assert os.path.exists(pdf_path)
    with open(pdf_path, "rb") as f:
        content = f.read()
    text = extract_document_text("Dr_Elena_Rostova_AI_NLP_Resume.pdf", content)
    assert len(text) > 50
    assert "Elena Rostova" in text or "NLP" in text
