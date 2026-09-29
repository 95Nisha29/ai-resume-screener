"""Tests for NLP preprocessing and skill extraction."""

import pytest
from app.services.nlp import (
    clean_text,
    tokenize,
    extract_skills,
    extract_candidate_name,
    extract_contact_info,
    extract_experience_years,
    extract_education
)


def test_clean_text():
    raw = "Senior Engineer with C++, C#, and .NET! Visit https://github.com/test."
    cleaned = clean_text(raw)
    assert "cpp" in cleaned
    assert "csharp" in cleaned
    assert "dotnet" in cleaned
    assert "https" not in cleaned


def test_tokenize():
    text = "Experienced with React and Node.js for modern web development"
    tokens = tokenize(text, remove_stopwords=True)
    assert "react" in tokens
    assert "modern" in tokens
    assert "and" not in tokens  # Stopword removed


def test_extract_skills():
    text = "We require experience in Python, PyTorch, Docker, Kubernetes, and PostgreSQL."
    result = extract_skills(text)
    skills = result["skills"]
    assert "Python" in skills
    assert "PyTorch" in skills
    assert "Docker" in skills
    assert "Kubernetes" in skills
    assert "PostgreSQL" in skills
    assert "AI, ML & Data Science" in result["categories"]


def test_extract_contact_info():
    text = "Jane Doe | Email: jane.doe@example.com | Phone: (555) 123-4567"
    contact = extract_contact_info(text)
    assert contact["email"] == "jane.doe@example.com"
    assert "123-4567" in contact["phone"]


def test_extract_experience_years():
    text1 = "Senior Full Stack Engineer with 6+ years of experience building software."
    assert extract_experience_years(text1) == 6.0

    text2 = "Software Engineer (2019 - 2024)"
    assert extract_experience_years(text2) == 5.0


def test_extract_education():
    text_phd = "Holds a Ph.D. in Computer Science from MIT"
    assert extract_education(text_phd) == "Ph.D. / Doctorate"

    text_bs = "Earned a Bachelor of Science in Information Technology"
    assert extract_education(text_bs) == "Bachelor's Degree"
