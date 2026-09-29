"""FastAPI route definitions for candidate ranking and resume screening."""

import json
from typing import List, Optional
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from app.models.schemas import (
    ScreeningResponse,
    AnalyzeJDRequest,
    JobAnalysis
)
from app.services.extractor import extract_document_text
from app.services.nlp import extract_skills, extract_experience_years
from app.services.ranker import CandidateRanker
from app.services.sample_data import SAMPLE_JOB_DESCRIPTIONS, SAMPLE_RESUMES

router = APIRouter()


@router.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "AI Resume Screening & Candidate Ranking System",
        "version": "1.0.0"
    }


@router.get("/samples")
async def get_samples():
    """Retrieve pre-loaded realistic job descriptions and resumes for testing."""
    return {
        "job_descriptions": SAMPLE_JOB_DESCRIPTIONS,
        "resumes": [
            {
                "id": r["id"],
                "filename": r["filename"],
                "preview": r["text"][:300].strip() + "..."
            }
            for r in SAMPLE_RESUMES
        ]
    }


@router.post("/analyze-jd")
async def analyze_job_description(
    job_description: Optional[str] = Form(None),
    job_file: Optional[UploadFile] = File(None)
):
    """Analyze a job description and extract recognized skills and experience requirements."""
    text = ""
    if job_file and job_file.filename:
        content = await job_file.read()
        text = extract_document_text(job_file.filename, content)
    elif job_description:
        text = job_description

    if not text.strip():
        raise HTTPException(status_code=400, detail="Job description text or file is required.")

    skills_data = extract_skills(text)
    exp_req = extract_experience_years(text)

    return {
        "skills": skills_data["skills"],
        "categories": skills_data["categories"],
        "total_skills_count": len(skills_data["skills"]),
        "required_experience_years": exp_req
    }


@router.post("/rank", response_model=ScreeningResponse)
async def rank_resumes(
    job_description: Optional[str] = Form(None),
    job_file: Optional[UploadFile] = File(None),
    resumes: List[UploadFile] = File(...),
    weight_similarity: float = Form(0.40),
    weight_skills: float = Form(0.45),
    weight_experience: float = Form(0.15)
):
    """
    Parse uploaded resumes (PDF, DOCX, TXT) and rank them against the Job Description.
    """
    # 1. Extract Job Description text
    jd_text = ""
    if job_file and job_file.filename:
        content = await job_file.read()
        jd_text = extract_document_text(job_file.filename, content)
    elif job_description:
        jd_text = job_description

    if not jd_text.strip():
        raise HTTPException(
            status_code=400,
            detail="Job description text or file is required."
        )

    if not resumes:
        raise HTTPException(
            status_code=400,
            detail="At least one candidate resume file is required."
        )

    # 2. Extract text from uploaded resumes
    parsed_resumes = []
    for idx, file in enumerate(resumes):
        if not file.filename:
            continue
        try:
            content = await file.read()
            extracted = extract_document_text(file.filename, content)
            if extracted.strip():
                parsed_resumes.append({
                    "id": f"uploaded-{idx+1}",
                    "filename": file.filename,
                    "text": extracted
                })
        except Exception as e:
            # Continue on single failure
            continue

    if not parsed_resumes:
        raise HTTPException(
            status_code=400,
            detail="Could not extract readable text from any of the provided resume files. Check file formats (PDF, DOCX, TXT)."
        )

    # 3. Perform candidate ranking
    ranker = CandidateRanker(
        weight_similarity=weight_similarity,
        weight_skills=weight_skills,
        weight_experience=weight_experience
    )

    result = ranker.rank_candidates(jd_text, parsed_resumes)
    return {"success": True, **result}


@router.post("/rank-samples", response_model=ScreeningResponse)
async def rank_sample_candidates(
    sample_jd_id: str = Form("jd-fullstack"),
    weight_similarity: float = Form(0.40),
    weight_skills: float = Form(0.45),
    weight_experience: float = Form(0.15)
):
    """Rank preloaded sample candidates against a selected sample job description."""
    # Find matching sample JD
    selected_jd = next((jd for jd in SAMPLE_JOB_DESCRIPTIONS if jd["id"] == sample_jd_id), None)
    if not selected_jd:
        selected_jd = SAMPLE_JOB_DESCRIPTIONS[0]

    ranker = CandidateRanker(
        weight_similarity=weight_similarity,
        weight_skills=weight_skills,
        weight_experience=weight_experience
    )

    result = ranker.rank_candidates(selected_jd["description"], SAMPLE_RESUMES)
    return {"success": True, **result}
