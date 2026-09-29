"""Tests for the Candidate Ranking Algorithm."""

import pytest
from app.services.ranker import CandidateRanker
from app.services.sample_data import SAMPLE_JOB_DESCRIPTIONS, SAMPLE_RESUMES


def test_ranking_algorithm_order():
    ranker = CandidateRanker()
    # Test against Full-Stack JD
    fs_jd = SAMPLE_JOB_DESCRIPTIONS[0]["description"]
    
    result = ranker.rank_candidates(fs_jd, SAMPLE_RESUMES)
    
    assert "ranked_candidates" in result
    candidates = result["ranked_candidates"]
    assert len(candidates) == len(SAMPLE_RESUMES)
    
    # Candidate #1 for FullStack should be Alex Rivera
    top_candidate = candidates[0]
    assert "Alex Rivera" in top_candidate["name"]
    assert top_candidate["score"] > 70.0
    assert top_candidate["tier"] in ("Strong Match", "Moderate Match")
    
    # Check that skills are properly separated into matched and missing
    assert len(top_candidate["matched_skills"]) > 0
    assert "React" in top_candidate["matched_skills"] or "TypeScript" in top_candidate["matched_skills"]
    
    # Lowest candidate should be the junior intern (Jordan Taylor)
    bottom_candidate = candidates[-1]
    assert "Jordan Taylor" in bottom_candidate["name"]
    assert bottom_candidate["score"] < top_candidate["score"]


def test_ranking_with_custom_weights():
    # Only skill match matters (100% skills weight)
    skill_heavy_ranker = CandidateRanker(
        weight_similarity=0.0,
        weight_skills=1.0,
        weight_experience=0.0
    )
    fs_jd = SAMPLE_JOB_DESCRIPTIONS[0]["description"]
    result = skill_heavy_ranker.rank_candidates(fs_jd, SAMPLE_RESUMES)
    candidates = result["ranked_candidates"]
    assert candidates[0]["breakdown"]["weights"]["skill_weight"] == 100.0
