# AI Resume Screening & Candidate Ranking System (TalentMatch AI)

An end-to-end intelligent recruitment system that analyzes candidate resumes against target job descriptions using **Natural Language Processing (NLP)**, **TF-IDF Vectorization**, and **Cosine Similarity**, producing an interpretable candidate ranking leaderboard with skill gap analysis.

---

## 🎯 Key Features

1. **Multi-Format Document Parsing**:
   - Seamlessly extracts text from **PDF**, **DOCX**, and **TXT** resume files.
   - Built-in fallback decoders for varied character encodings.

2. **NLP Preprocessing & Feature Extraction**:
   - Noise filtering, lowercasing, email, and phone number regex extraction.
   - Tokenization with domain-specific stopword removal (filtering resume boilerplate).
   - Multi-word N-Gram extraction for composite technical terminology.
   - **Comprehensive Skill Taxonomy**: 400+ categorized technical, cloud, data science, framework, database, and soft skills.
   - Heuristic candidate metadata extraction: Name, email, phone, detected experience years, and highest education credential.

3. **TF-IDF & Cosine Similarity Scoring Engine**:
   - Sublinear term-frequency scaling and unigram/bigram token vectors.
   - Pairwise Cosine Similarity matrix evaluating how closely candidate text matches the job description vocabulary.

4. **Composite Candidate Ranking Algorithm**:
   - Weighted scoring synthesis:
     $$\text{Final Score} = (w_{\text{similarity}} \cdot S_{\text{cosine}} + w_{\text{skills}} \cdot S_{\text{skills}} + w_{\text{experience}} \cdot S_{\text{exp}}) \times 100$$
   - **Explainable Skill Gap Analysis**:
     - 🟢 **Matched Skills**: Direct overlap between JD requirements and candidate profile.
     - 🔴 **Missing Skills**: Critical qualification gaps highlighted for recruiters.
     - 🔵 **Bonus Skills**: Additional domain-relevant candidate qualifications.
   - Customizable weight sliders via UI.

5. **Recruiter Dashboard UI**:
   - Modern, responsive Single Page Application (SPA) styled with Tailwind CSS and Lucide icons.
   - Preset Job Descriptions (*Full-Stack*, *ML/NLP*, *DevOps*).
   - Multi-file drag-and-drop resume upload zone.
   - One-click "Load 5 Demo Resumes" button for instant live testing.
   - Top candidate winner spotlight card.
   - Real-time candidate search and skill filtering.
   - Detailed modal deep-dive for every candidate.
   - One-click export to CSV.

---

## 🚀 Quick Start Guide

### 1. Prerequisites
- **Python 3.12+** installed on Windows.

### 2. Activate Virtual Environment
Open PowerShell inside the project directory:
```powershell
cd "C:\Users\Nisha Jogdand\.gemini\antigravity\scratch\ai_resume_screener"
.\.venv\Scripts\Activate.ps1
```

### 3. Run the Server
```powershell
.\.venv\Scripts\python.exe run.py
```

### 4. Access the Application
- **Recruiter Dashboard**: [http://127.0.0.1:8000](http://127.0.0.1:8000)
- **Interactive Swagger API Docs**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## 🧪 Running Automated Tests

Run the test suite:
```powershell
.\.venv\Scripts\python.exe -m pytest tests/ -v
```
All 17 tests verify document parsing, NLP extraction, TF-IDF cosine similarity, ranking logic, and API endpoints.

---

## 📁 Project Architecture

```
ai_resume_screener/
├── requirements.txt            # Project dependencies
├── run.py                      # Uvicorn server launcher
├── README.md                   # Project documentation
├── app/
│   ├── main.py                 # FastAPI application & static route config
│   ├── api/
│   │   └── routes.py           # REST endpoints (/api/rank, /api/analyze-jd, etc.)
│   ├── models/
│   │   └── schemas.py          # Pydantic data validation schemas
│   ├── services/
│   │   ├── extractor.py        # PDF, DOCX, TXT text extraction
│   │   ├── nlp.py              # NLP cleaning, tokenization, skill taxonomy
│   │   ├── similarity.py       # TF-IDF vectorizer & Cosine similarity
│   │   ├── ranker.py           # Composite candidate ranking algorithm
│   │   └── sample_data.py      # Preloaded sample JDs & candidate profiles
│   └── static/                 # Web Frontend
│       ├── index.html          # Recruiter dashboard SPA
│       ├── css/style.css       # Custom styles & animations
│       └── js/app.js           # Client application logic & CSV export
├── sample_data/                # Standalone sample files (.pdf, .docx, .txt)
└── tests/                      # Automated test suite (17 tests)
```
