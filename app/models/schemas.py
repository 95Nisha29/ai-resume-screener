"""Pydantic schemas for request and response models."""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class ScoringWeights(BaseModel):
    similarity: float = Field(default=0.40, ge=0.0, le=1.0, description="Weight for TF-IDF Cosine Similarity")
    skills: float = Field(default=0.45, ge=0.0, le=1.0, description="Weight for Skill Match Ratio")
    experience: float = Field(default=0.15, ge=0.0, le=1.0, description="Weight for Experience & Education Match")


class AnalyzeJDRequest(BaseModel):
    job_description: str = Field(..., min_length=10, description="Job description text to analyze")


class ScoreBreakdown(BaseModel):
    similarity_score: float
    skill_score: float
    experience_score: float
    weights: Dict[str, float]


class CandidateResult(BaseModel):
    rank: int
    id: str
    name: str
    filename: str
    score: float
    tier: str
    tier_color: str
    email: Optional[str] = None
    phone: Optional[str] = None
    experience_years: float
    education: str
    matched_skills: List[str]
    missing_skills: List[str]
    additional_skills: List[str]
    total_skills_count: int
    matched_skills_count: int
    breakdown: ScoreBreakdown
    snippet: str


class JobAnalysis(BaseModel):
    skills: List[str]
    categories: Dict[str, List[str]]
    total_skills_count: int
    required_experience_years: float


class SummaryMetrics(BaseModel):
    total_candidates: int
    avg_score: float
    top_score: float
    strong_matches: int
    moderate_matches: int
    low_matches: int


class ScreeningResponse(BaseModel):
    success: bool = True
    job_analysis: JobAnalysis
    ranked_candidates: List[CandidateResult]
    summary_metrics: SummaryMetrics
