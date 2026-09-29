"""Tests for FastAPI endpoints."""

import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"


def test_samples_endpoint():
    response = client.get("/api/samples")
    assert response.status_code == 200
    data = response.json()
    assert "job_descriptions" in data
    assert len(data["job_descriptions"]) >= 3
    assert "resumes" in data
    assert len(data["resumes"]) >= 5


def test_analyze_jd_endpoint():
    payload = {"job_description": "We are seeking a Python engineer with FastAPI, Docker, and PostgreSQL experience. 3+ years required."}
    response = client.post("/api/analyze-jd", data=payload)
    assert response.status_code == 200
    data = response.json()
    assert "Python" in data["skills"]
    assert "FastAPI" in data["skills"]
    assert "Docker" in data["skills"]
    assert data["required_experience_years"] == 3.0


def test_rank_samples_endpoint():
    response = client.post("/api/rank-samples", data={"sample_jd_id": "jd-fullstack"})
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert len(data["ranked_candidates"]) > 0
    assert data["ranked_candidates"][0]["rank"] == 1
