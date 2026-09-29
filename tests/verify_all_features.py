"""Comprehensive feature verification script for TalentMatch AI."""

import sys
import json
import httpx

BASE_URL = "http://127.0.0.1:8000"

def run_checks():
    client = httpx.Client(base_url=BASE_URL, timeout=10.0)
    results = []

    # 1. Health check
    try:
        r = client.get("/health")
        assert r.status_code == 200
        data = r.json()
        assert data.get("status") == "healthy"
        results.append(("Health Check API (/health)", "PASSED", f"Status: {data.get('status')}"))
    except Exception as e:
        results.append(("Health Check API (/health)", "FAILED", str(e)))

    # 2. Web UI frontend
    try:
        r = client.get("/")
        assert r.status_code == 200
        assert "TalentMatch AI" in r.text
        assert "Candidate Leaderboard" in r.text
        assert "drop-zone" in r.text
        results.append(("Web Frontend UI (/) Serving", "PASSED", f"Loaded {len(r.text)} bytes of HTML/CSS/JS"))
    except Exception as e:
        results.append(("Web Frontend UI (/) Serving", "FAILED", str(e)))

    # 3. Sample data API
    try:
        r = client.get("/api/samples")
        assert r.status_code == 200
        data = r.json()
        jds = data.get("job_descriptions", [])
        resumes = data.get("resumes", [])
        assert len(jds) >= 3
        assert len(resumes) >= 5
        results.append(("Sample Data API (/api/samples)", "PASSED", f"{len(jds)} preset roles, {len(resumes)} sample candidates"))
    except Exception as e:
        results.append(("Sample Data API (/api/samples)", "FAILED", str(e)))

    # 4. Job Description Skill Extraction
    try:
        payload = {"job_description": "We need a Senior Backend Developer with Python, FastAPI, Docker, and PostgreSQL. 4+ years of experience required."}
        r = client.post("/api/analyze-jd", data=payload)
        assert r.status_code == 200
        data = r.json()
        skills = data.get("skills", [])
        exp = data.get("required_experience_years")
        assert "Python" in skills
        assert "FastAPI" in skills
        assert "Docker" in skills
        assert "PostgreSQL" in skills
        assert exp == 4.0
        results.append(("NLP JD Skill Extraction (/api/analyze-jd)", "PASSED", f"Detected: {skills} | Required Exp: {exp} yrs"))
    except Exception as e:
        results.append(("NLP JD Skill Extraction (/api/analyze-jd)", "FAILED", str(e)))

    # 5. Full-Stack Demo Ranking
    try:
        r = client.post("/api/rank-samples", data={"sample_jd_id": "jd-fullstack"})
        assert r.status_code == 200
        data = r.json()
        ranked = data.get("ranked_candidates", [])
        assert len(ranked) >= 5
        top = ranked[0]
        assert "Alex Rivera" in top["name"]
        assert top["score"] > 65.0
        assert len(top["matched_skills"]) > 5
        results.append(("Demo Full-Stack Role Ranking (/api/rank-samples)", "PASSED", f"#1 Rank: {top['name']} ({top['score']}%)"))
    except Exception as e:
        results.append(("Demo Full-Stack Role Ranking (/api/rank-samples)", "FAILED", str(e)))

    # 6. ML / NLP Demo Ranking
    try:
        r = client.post("/api/rank-samples", data={"sample_jd_id": "jd-ml"})
        assert r.status_code == 200
        data = r.json()
        top = data["ranked_candidates"][0]
        assert "Elena Rostova" in top["name"]
        results.append(("Demo ML / NLP Role Ranking (/api/rank-samples)", "PASSED", f"#1 Rank: {top['name']} ({top['score']}%)"))
    except Exception as e:
        results.append(("Demo ML / NLP Role Ranking (/api/rank-samples)", "FAILED", str(e)))

    # 7. DevOps Demo Ranking
    try:
        r = client.post("/api/rank-samples", data={"sample_jd_id": "jd-devops"})
        assert r.status_code == 200
        data = r.json()
        top = data["ranked_candidates"][0]
        assert "Marcus Chen" in top["name"]
        results.append(("Demo DevOps Role Ranking (/api/rank-samples)", "PASSED", f"#1 Rank: {top['name']} ({top['score']}%)"))
    except Exception as e:
        results.append(("Demo DevOps Role Ranking (/api/rank-samples)", "FAILED", str(e)))

    # 8. Multi-format Custom File Upload (DOCX, PDF, TXT)
    try:
        jd_text = open("sample_data/job_descriptions/Senior_FullStack_Engineer_JD.txt", "r", encoding="utf-8").read()
        docx_file = ("Alex.docx", open("sample_data/resumes/Alex_Rivera_FullStack_Resume.docx", "rb"), "application/vnd.openxmlformats-officedocument.wordprocessingml.document")
        pdf_file = ("Elena.pdf", open("sample_data/resumes/Dr_Elena_Rostova_AI_NLP_Resume.pdf", "rb"), "application/pdf")
        txt_file = ("Jordan.txt", open("sample_data/resumes/Jordan_Taylor_Junior_Web_Resume.txt", "rb"), "text/plain")

        files = [("resumes", docx_file), ("resumes", pdf_file), ("resumes", txt_file)]
        r = client.post("/api/rank", data={"job_description": jd_text}, files=files)
        assert r.status_code == 200
        data = r.json()
        ranked = data.get("ranked_candidates", [])
        assert len(ranked) == 3
        results.append(("Multi-format File Upload (PDF, DOCX, TXT)", "PASSED", f"Screened {len(ranked)} files. Top: {ranked[0]['name']} ({ranked[0]['score']}%)"))
    except Exception as e:
        results.append(("Multi-format File Upload (PDF, DOCX, TXT)", "FAILED", str(e)))

    # 9. Dynamic Custom Weight Adjustments
    try:
        # Weight similarity high vs skill high
        r_sim = client.post("/api/rank-samples", data={"sample_jd_id": "jd-fullstack", "weight_similarity": 0.80, "weight_skills": 0.10, "weight_experience": 0.10})
        r_skl = client.post("/api/rank-samples", data={"sample_jd_id": "jd-fullstack", "weight_similarity": 0.10, "weight_skills": 0.80, "weight_experience": 0.10})
        score_sim = r_sim.json()["ranked_candidates"][0]["score"]
        score_skl = r_skl.json()["ranked_candidates"][0]["score"]
        assert score_sim != score_skl
        results.append(("Configurable Scoring Weights Engine", "PASSED", f"Sim-heavy: {score_sim}% vs Skill-heavy: {score_skl}%"))
    except Exception as e:
        results.append(("Configurable Scoring Weights Engine", "FAILED", str(e)))

    # Print Summary Table
    print("\n" + "=" * 70)
    print(f"{'FEATURE':<45} | {'STATUS':<8} | DETAILS")
    print("=" * 70)
    all_passed = True
    for feat, status, detail in results:
        print(f"{feat:<45} | {status:<8} | {detail}")
        if status != "PASSED":
            all_passed = False
    print("=" * 70)
    print(f"Overall Result: {'ALL 9 FEATURES OPERATIONAL' if all_passed else 'SOME CHECKS FAILED'}\n")
    return all_passed

if __name__ == "__main__":
    success = run_checks()
    sys.exit(0 if success else 1)
