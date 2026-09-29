"""Candidate Ranking Algorithm with multi-factor scoring and skill gap analysis."""

from typing import List, Dict, Any, Optional
from app.services.nlp import (
    extract_skills,
    extract_candidate_name,
    extract_contact_info,
    extract_experience_years,
    extract_education,
    clean_text
)
from app.services.similarity import SimilarityEngine


class CandidateRanker:
    """Ranks candidates by analyzing resumes against a job description."""

    def __init__(
        self,
        weight_similarity: float = 0.40,
        weight_skills: float = 0.45,
        weight_experience: float = 0.15
    ):
        # Normalize weights so sum is 1.0
        total = weight_similarity + weight_skills + weight_experience
        if total <= 0:
            total = 1.0
        self.w_sim = weight_similarity / total
        self.w_skill = weight_skills / total
        self.w_exp = weight_experience / total
        self.similarity_engine = SimilarityEngine()

    def rank_candidates(
        self,
        job_description: str,
        resumes: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Rank a collection of candidate resumes against a job description.

        Args:
            job_description: Plain text of the job description.
            resumes: List of dicts with:
                - 'id': unique identifier
                - 'filename': name of file
                - 'text': raw extracted resume text

        Returns:
            Dict containing:
                - 'job_analysis': extracted skills and experience requirement from JD
                - 'ranked_candidates': list of candidate assessment dicts sorted by score
                - 'summary_metrics': total candidates, average score, top candidate
        """
        if not resumes:
            return {
                "job_analysis": {"skills": [], "required_experience_years": 0.0},
                "ranked_candidates": [],
                "summary_metrics": {
                    "total_candidates": 0,
                    "avg_score": 0.0,
                    "top_score": 0.0
                }
            }

        # 1. Analyze Job Description
        jd_skills_data = extract_skills(job_description)
        jd_skills_set = set(jd_skills_data["skills"])
        jd_exp_req = extract_experience_years(job_description)

        # 2. Compute TF-IDF Cosine Similarity for all resumes
        resume_texts = [r.get("text", "") for r in resumes]
        similarity_scores = self.similarity_engine.compute_similarities(job_description, resume_texts)

        evaluated_candidates = []

        for idx, resume_item in enumerate(resumes):
            raw_text = resume_item.get("text", "")
            filename = resume_item.get("filename", f"Resume_{idx+1}")
            cid = resume_item.get("id", str(idx + 1))

            # NLP Extraction on Resume
            cand_skills_data = extract_skills(raw_text)
            cand_skills_set = set(cand_skills_data["skills"])
            
            contact = extract_contact_info(raw_text)
            name = extract_candidate_name(raw_text, filename=filename)
            exp_years = extract_experience_years(raw_text)
            education = extract_education(raw_text)

            # Skill Gap Analysis
            matched_skills = sorted(list(jd_skills_set.intersection(cand_skills_set)))
            missing_skills = sorted(list(jd_skills_set.difference(cand_skills_set)))
            additional_skills = sorted(list(cand_skills_set.difference(jd_skills_set)))

            # Skill Score Computation
            if jd_skills_set:
                skill_ratio = len(matched_skills) / len(jd_skills_set)
                # Small bonus for depth of additional relevant skills (capped at +10%)
                bonus = min(len(additional_skills) * 0.01, 0.10)
                skill_score = min(skill_ratio + bonus, 1.0)
            else:
                # If JD didn't have explicitly recognized skills, fallback to text similarity
                skill_score = similarity_scores[idx]

            # Experience Score Computation
            if jd_exp_req > 0:
                if exp_years >= jd_exp_req:
                    exp_score = 1.0
                elif exp_years > 0:
                    exp_score = max(0.2, exp_years / jd_exp_req)
                else:
                    exp_score = 0.3  # Unknown / unstated experience
            else:
                # No specific experience required, baseline score based on detected presence
                exp_score = 1.0 if exp_years >= 2.0 else 0.8

            tfidf_score = similarity_scores[idx]

            # Composite Final Score (0 - 100)
            composite_score = (
                (self.w_sim * tfidf_score) +
                (self.w_skill * skill_score) +
                (self.w_exp * exp_score)
            ) * 100.0
            
            final_score = round(float(composite_score), 1)

            # Match Tier
            if final_score >= 75.0:
                tier = "Strong Match"
                tier_color = "emerald"
            elif final_score >= 50.0:
                tier = "Moderate Match"
                tier_color = "amber"
            else:
                tier = "Low Match"
                tier_color = "rose"

            evaluated_candidates.append({
                "id": cid,
                "name": name,
                "filename": filename,
                "score": final_score,
                "tier": tier,
                "tier_color": tier_color,
                "email": contact["email"],
                "phone": contact["phone"],
                "experience_years": exp_years,
                "education": education,
                "matched_skills": matched_skills,
                "missing_skills": missing_skills,
                "additional_skills": additional_skills[:10],
                "total_skills_count": len(cand_skills_set),
                "matched_skills_count": len(matched_skills),
                "breakdown": {
                    "similarity_score": round(tfidf_score * 100.0, 1),
                    "skill_score": round(skill_score * 100.0, 1),
                    "experience_score": round(exp_score * 100.0, 1),
                    "weights": {
                        "similarity_weight": round(self.w_sim * 100, 1),
                        "skill_weight": round(self.w_skill * 100, 1),
                        "experience_weight": round(self.w_exp * 100, 1)
                    }
                },
                "snippet": raw_text[:400].strip() + ("..." if len(raw_text) > 400 else "")
            })

        # Sort descending by score
        ranked_candidates = sorted(
            evaluated_candidates,
            key=lambda c: c["score"],
            reverse=True
        )

        # Assign rank positions
        for rank, cand in enumerate(ranked_candidates, start=1):
            cand["rank"] = rank

        scores = [c["score"] for c in ranked_candidates]
        avg_score = round(sum(scores) / len(scores), 1) if scores else 0.0
        top_score = scores[0] if scores else 0.0

        return {
            "job_analysis": {
                "skills": sorted(list(jd_skills_set)),
                "categories": jd_skills_data["categories"],
                "total_skills_count": len(jd_skills_set),
                "required_experience_years": jd_exp_req
            },
            "ranked_candidates": ranked_candidates,
            "summary_metrics": {
                "total_candidates": len(ranked_candidates),
                "avg_score": avg_score,
                "top_score": top_score,
                "strong_matches": sum(1 for c in ranked_candidates if c["score"] >= 75.0),
                "moderate_matches": sum(1 for c in ranked_candidates if 50.0 <= c["score"] < 75.0),
                "low_matches": sum(1 for c in ranked_candidates if c["score"] < 50.0)
            }
        }
