"""Tests for TF-IDF vectorization and Cosine Similarity."""

import pytest
from app.services.similarity import SimilarityEngine


def test_similarity_identical():
    engine = SimilarityEngine()
    jd = "Python FastAPI Docker Kubernetes PostgreSQL"
    resumes = [jd]
    scores = engine.compute_similarities(jd, resumes)
    assert len(scores) == 1
    assert scores[0] > 0.95  # Identical texts should have ~1.0 cosine similarity


def test_similarity_relative_ordering():
    engine = SimilarityEngine()
    jd = "Machine Learning Engineer with deep learning, PyTorch, Transformers, NLP, and model deployment."
    
    ml_resume = "Data scientist specializing in machine learning, deep learning, PyTorch, and NLP models."
    unrelated_resume = "Pastry chef with experience in baking sourdough bread, wedding cakes, and kitchen management."

    scores = engine.compute_similarities(jd, [ml_resume, unrelated_resume])
    assert scores[0] > scores[1]
    assert scores[0] > 0.25
    assert scores[1] < 0.10
