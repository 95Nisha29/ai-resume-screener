"""
================================================================================
  TALENTMATCH AI - COMPLETE ALL-IN-ONE SYSTEM
  AI Resume Screening & Candidate Ranking System (Single Executable File)
================================================================================

HOW TO RUN IN TERMINAL:
  1. Install required packages (one time):
     pip install fastapi uvicorn pydantic scikit-learn numpy python-multipart pypdf python-docx

  2. Run the command in your terminal:
     python app_combined.py

  3. That's it! It will launch the server and automatically open the website
     in your browser at: http://127.0.0.1:8000
================================================================================
"""

import io
import os
import re
import sys
import threading
import time
import webbrowser
from typing import Dict, List, Set, Tuple, Optional, Any, Union, BinaryIO

import numpy as np
from pydantic import BaseModel, Field
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
import uvicorn

# ==============================================================================
# 1. NLP PREPROCESSING, STOPWORDS & 400+ SKILL TAXONOMY
# ==============================================================================

STOPWORDS: Set[str] = {
    "a", "about", "above", "after", "again", "against", "all", "am", "an", "and", "any", "are", 
    "aren", "as", "at", "be", "because", "been", "before", "being", "below", "between", "both", 
    "but", "by", "can", "cannot", "could", "couldn", "did", "didn", "do", "does", "doesn", 
    "doing", "don", "down", "during", "each", "few", "for", "from", "further", "had", "hadn", 
    "has", "hasn", "have", "haven", "having", "he", "her", "here", "hers", "herself", "him", 
    "himself", "his", "how", "if", "in", "into", "is", "isn", "it", "its", "itself", "just", 
    "me", "more", "most", "mustn", "my", "myself", "no", "nor", "not", "of", "off", "on", 
    "once", "only", "or", "other", "ought", "our", "ours", "ourselves", "out", "over", "own", 
    "same", "shan", "she", "should", "shouldn", "so", "some", "such", "than", "that", "the", 
    "their", "theirs", "them", "themselves", "then", "there", "these", "they", "this", "those", 
    "through", "to", "too", "under", "until", "up", "very", "was", "wasn", "we", "were", 
    "weren", "what", "when", "where", "which", "while", "who", "whom", "why", "with", "won", 
    "would", "wouldn", "you", "your", "yours", "yourself", "yourselves",
    "resume", "curriculum", "vitae", "cv", "page", "phone", "email", "contact", "address", 
    "date", "year", "years", "month", "months", "responsible", "duties", "including", "work", 
    "experience", "summary", "profile", "objective", "skills", "skill", "education"
}

SKILL_TAXONOMY: Dict[str, Dict[str, List[str]]] = {
    "Programming Languages": {
        "Python": ["python", "python3", "py"],
        "JavaScript": ["javascript", "js", "ecmascript"],
        "TypeScript": ["typescript", "ts"],
        "Java": ["java", "j2ee"],
        "C++": ["c++", "cpp"],
        "C#": ["c#", "csharp", ".net c#"],
        "C": ["c programming", "c lang"],
        "Go": ["golang", "go programming", "go"],
        "Rust": ["rust", "rust-lang"],
        "Ruby": ["ruby"],
        "PHP": ["php", "php7", "php8"],
        "Swift": ["swift"],
        "Kotlin": ["kotlin"],
        "Scala": ["scala"],
        "R": ["r programming", "r language", "r-lang"],
        "SQL": ["sql", "structured query language"],
        "HTML/CSS": ["html", "html5", "css", "css3", "sass", "scss", "less"],
        "Shell/Bash": ["bash", "shell scripting", "powershell", "sh", "zsh"],
        "Dart": ["dart"],
        "Solidity": ["solidity", "web3"]
    },
    "Frontend & Web": {
        "React": ["react", "react.js", "reactjs"],
        "Next.js": ["next.js", "nextjs", "next"],
        "Vue.js": ["vue", "vue.js", "vuejs", "vue3"],
        "Angular": ["angular", "angular.js", "angularjs", "angular 2+"],
        "Svelte": ["svelte", "sveltekit"],
        "Redux": ["redux", "redux toolkit", "rtk"],
        "Tailwind CSS": ["tailwind", "tailwindcss", "tailwind css"],
        "Bootstrap": ["bootstrap", "bootstrap5"],
        "Webpack/Vite": ["webpack", "vite", "babel", "esbuild"],
        "GraphQL Client": ["apollo client", "relay"],
        "WebSockets": ["websocket", "websockets", "socket.io"]
    },
    "Backend & APIs": {
        "FastAPI": ["fastapi", "fast-api"],
        "Django": ["django", "django rest framework", "drf"],
        "Flask": ["flask"],
        "Node.js": ["node", "node.js", "nodejs"],
        "Express.js": ["express", "express.js", "expressjs"],
        "NestJS": ["nestjs", "nest.js"],
        "Spring Boot": ["spring boot", "springboot", "spring framework", "spring"],
        "ASP.NET": ["asp.net", "asp.net core", ".net core", "dotnet"],
        "Ruby on Rails": ["ruby on rails", "rails"],
        "RESTful API": ["rest", "rest api", "restful", "restful api", "restful apis", "rest apis"],
        "GraphQL": ["graphql", "graphql api"],
        "gRPC": ["grpc", "protobuf"],
        "Microservices": ["microservices", "microservice architecture", "micro-services"]
    },
    "AI, ML & Data Science": {
        "Machine Learning": ["machine learning", "ml", "statistical learning"],
        "Deep Learning": ["deep learning", "dl", "neural networks", "ann", "cnn", "rnn", "lstm"],
        "Natural Language Processing": ["nlp", "natural language processing", "text mining", "ner", "sentiment analysis"],
        "Computer Vision": ["computer vision", "cv", "opencv", "object detection", "image segmentation"],
        "Large Language Models": ["llm", "llms", "large language models", "generative ai", "genai", "prompt engineering", "rag"],
        "LangChain": ["langchain", "langsmith", "llamaindex"],
        "PyTorch": ["pytorch", "torch"],
        "TensorFlow": ["tensorflow", "tf", "keras"],
        "Scikit-Learn": ["scikit-learn", "sklearn"],
        "Pandas": ["pandas"],
        "NumPy": ["numpy"],
        "Transformers": ["transformers", "huggingface", "hugging face", "bert", "gpt"],
        "Data Analysis": ["data analysis", "eda", "exploratory data analysis", "data analytics"],
        "Data Visualization": ["data visualization", "matplotlib", "seaborn", "tableau", "power bi", "powerbi", "plotly"],
        "Big Data": ["spark", "apache spark", "pyspark", "hadoop", "flink", "databricks"],
        "Feature Engineering": ["feature engineering", "data preprocessing", "model evaluation"]
    },
    "Databases & Caching": {
        "PostgreSQL": ["postgresql", "postgres", "psql"],
        "MySQL": ["mysql", "mariadb"],
        "MongoDB": ["mongodb", "mongo"],
        "Redis": ["redis"],
        "Elasticsearch": ["elasticsearch", "elastic search", "opensearch"],
        "SQLite": ["sqlite", "sqlite3"],
        "Cassandra": ["cassandra", "apache cassandra"],
        "DynamoDB": ["dynamodb", "aws dynamodb"],
        "Snowflake": ["snowflake"],
        "BigQuery": ["bigquery", "google bigquery"],
        "Oracle": ["oracle db", "oracle sql"],
        "SQL Server": ["sql server", "mssql", "microsoft sql server"],
        "Neo4j": ["neo4j", "graph database"]
    },
    "Cloud & DevOps": {
        "AWS": ["aws", "amazon web services", "ec2", "s3", "lambda", "ecs", "eks", "rds", "cloudformation"],
        "Google Cloud (GCP)": ["gcp", "google cloud", "google cloud platform", "gke", "cloud run"],
        "Microsoft Azure": ["azure", "microsoft azure", "azure devops", "blob storage"],
        "Docker": ["docker", "containerization", "containers", "docker-compose"],
        "Kubernetes": ["kubernetes", "k8s"],
        "CI/CD": ["ci/cd", "ci cd", "continuous integration", "continuous deployment", "github actions", "gitlab ci", "jenkins"],
        "Terraform": ["terraform", "iac", "infrastructure as code"],
        "Linux": ["linux", "ubuntu", "debian", "centos", "redhat"],
        "Nginx": ["nginx", "apache web server"],
        "Ansible": ["ansible"],
        "Monitoring/Logging": ["prometheus", "grafana", "datadog", "elk stack", "splunk", "cloudwatch"]
    },
    "Software Engineering & Soft Skills": {
        "Git/GitHub": ["git", "github", "gitlab", "version control", "bitbucket"],
        "Agile/Scrum": ["agile", "scrum", "kanban", "sprint planning", "jira"],
        "Unit Testing": ["unit testing", "pytest", "jest", "junit", "tdd", "test driven development"],
        "System Design": ["system design", "software architecture", "scalability", "distributed systems", "high availability"],
        "Problem Solving": ["problem solving", "analytical skills", "critical thinking"],
        "Leadership/Mentoring": ["leadership", "team lead", "mentoring", "code review", "cross-functional"]
    }
}

ALIAS_TO_CANONICAL: Dict[str, str] = {}
CANONICAL_TO_CATEGORY: Dict[str, str] = {}

for category, skill_map in SKILL_TAXONOMY.items():
    for canonical, aliases in skill_map.items():
        CANONICAL_TO_CATEGORY[canonical] = category
        for alias in aliases:
            ALIAS_TO_CANONICAL[alias.lower()] = canonical
        ALIAS_TO_CANONICAL[canonical.lower()] = canonical

SORTED_ALIASES = sorted(ALIAS_TO_CANONICAL.keys(), key=lambda s: len(s), reverse=True)


def clean_text(text: str) -> str:
    """Normalize and clean raw text while keeping meaningful words."""
    if not text:
        return ""
    text = text.lower()
    text = re.sub(r"[\r\t\f\v]+", " ", text)
    text = re.sub(r"https?://\S+|www\.\S+", " ", text)
    text = re.sub(r"c\+\+", "cpp", text)
    text = re.sub(r"c\#", "csharp", text)
    text = re.sub(r"\.net\b", "dotnet", text)
    text = re.sub(r"[^\w\s\-]", " ", text)
    text = re.sub(r"\s-\s", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def extract_skills(text: str) -> Dict[str, List[str]]:
    """Extract recognized skills from text using phrase and regex matching."""
    if not text:
        return {"skills": [], "categories": {}}

    text_lower = " " + clean_text(text) + " "
    found_canonicals: Set[str] = set()

    for alias in SORTED_ALIASES:
        escaped_alias = re.escape(alias)
        pattern = rf"(?<![a-zA-Z0-9]){escaped_alias}(?![a-zA-Z0-9])"
        if re.search(pattern, text_lower):
            canonical = ALIAS_TO_CANONICAL[alias]
            found_canonicals.add(canonical)

    categorized: Dict[str, List[str]] = {}
    for skill in sorted(found_canonicals):
        category = CANONICAL_TO_CATEGORY.get(skill, "Other")
        categorized.setdefault(category, []).append(skill)

    return {
        "skills": sorted(list(found_canonicals)),
        "categories": categorized
    }


def extract_candidate_name(text: str, filename: Optional[str] = None) -> str:
    """Extract candidate name from top lines of resume or fallback to filename."""
    if not text:
        if filename:
            name = re.sub(r"\.(pdf|docx|txt)$", "", filename, flags=re.I)
            name = re.sub(r"[_\-]+", " ", name).title()
            return name
        return "Unknown Candidate"

    lines = [line.strip() for line in text.split("\n") if line.strip()]
    skip_headers = {
        "resume", "curriculum vitae", "cv", "profile", "contact", "summary",
        "professional summary", "career objective", "experience", "work experience",
        "education", "skills", "technical skills", "projects", "personal info"
    }

    for line in lines[:8]:
        line_clean = line.strip()
        if "@" in line_clean or re.search(r"\d{3,}", line_clean):
            continue
        if line_clean.lower() in skip_headers or len(line_clean) < 3 or len(line_clean) > 40:
            continue
        
        words = line_clean.split()
        cleaned_words = [re.sub(r"[,().]+", "", w).strip() for w in words]
        cleaned_words = [w for w in cleaned_words if w]
        name_words = [w for w in cleaned_words if w.lower() not in {"dr", "phd", "mr", "ms", "mrs", "prof", "md", "eng"}]
        if 2 <= len(name_words) <= 4 and all(w.isalpha() for w in name_words):
            return " ".join(name_words).title()

    if filename:
        name = re.sub(r"\.(pdf|docx|txt)$", "", filename, flags=re.I)
        name = re.sub(r"[_\-]+", " ", name)
        name = re.sub(r"\bresume\b|\bcv\b", "", name, flags=re.I).strip().title()
        if name:
            return name

    return "Candidate"


def extract_contact_info(text: str) -> Dict[str, Optional[str]]:
    """Extract email and phone number from text."""
    email_match = re.search(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b", text)
    phone_match = re.search(r"(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b", text)
    return {
        "email": email_match.group(0) if email_match else None,
        "phone": phone_match.group(0) if phone_match else None
    }


def extract_experience_years(text: str) -> float:
    """Extract estimated years of experience using regex patterns."""
    if not text:
        return 0.0

    text_lower = text.lower()
    direct_patterns = [
        r"(?:experience\s*:\s*|over\s+|at\s+least\s+|minimum\s+)?(\d+(?:\.\d+)?)\s*(?:\+)?\s*(?:years?|yrs?)(?:\s+of)?(?:\s+(?:professional\s+)?experience|\s+required|\s+in|\s+minimum)?\b",
        r"(\d+(?:\.\d+)?)\s*\+\s*(?:years?|yrs?)\b",
        r"(\d+(?:\.\d+)?)\s*(?:years?|yrs?)\s+required\b"
    ]

    for pat in direct_patterns:
        match = re.search(pat, text_lower)
        if match:
            try:
                val = float(match.group(1))
                if 0 < val <= 40:
                    return val
            except ValueError:
                pass

    year_ranges = re.findall(r"\b(200\d|201\d|202\d)\s*(?:-|to|–)\s*(200\d|201\d|202\d|present|current)\b", text_lower)
    if year_ranges:
        intervals = []
        for start_str, end_str in year_ranges:
            try:
                start = int(start_str)
                end = 2026 if end_str in ("present", "current") else int(end_str)
                if 1990 <= start <= end <= 2026:
                    intervals.append((start, end))
            except ValueError:
                continue

        if intervals:
            intervals.sort(key=lambda x: x[0])
            merged = [intervals[0]]
            for current in intervals[1:]:
                prev_start, prev_end = merged[-1]
                if current[0] <= prev_end:
                    merged[-1] = (prev_start, max(prev_end, current[1]))
                else:
                    merged.append(current)

            total_span = sum(end - start for start, end in merged)
            if 0 < total_span <= 40:
                return float(total_span)

    return 0.0


def extract_education(text: str) -> str:
    """Extract highest education credential detected."""
    text_lower = text.lower()
    if re.search(r"\b(ph\.?d|doctorate|doctor of philosophy)\b", text_lower):
        return "Ph.D. / Doctorate"
    elif re.search(r"\b(master'?s?|m\.?s\.?|m\.?tech|m\.?sc|mba|m\.?eng)\b", text_lower):
        return "Master's Degree"
    elif re.search(r"\b(bachelor'?s?|b\.?s\.?|b\.?tech|b\.?e\.?|b\.?sc|bba)\b", text_lower):
        return "Bachelor's Degree"
    elif re.search(r"\b(associate'?s?|diploma)\b", text_lower):
        return "Associate Degree / Diploma"
    else:
        return "Not Specified"


# ==============================================================================
# 2. DOCUMENT TEXT EXTRACTORS (PDF, DOCX, TXT)
# ==============================================================================

def extract_document_text(filename: str, content: Union[str, bytes, BinaryIO]) -> str:
    """Extract plain text from PDF, DOCX, or TXT file."""
    ext = os.path.splitext(filename.lower())[1]

    # PDF Parser
    if ext == ".pdf":
        try:
            from pypdf import PdfReader
            stream = io.BytesIO(content) if isinstance(content, (bytes, bytearray)) else content
            reader = PdfReader(stream)
            pages = [p.extract_text() or "" for p in reader.pages]
            return "\n\n".join([p.strip() for p in pages if p.strip()])
        except Exception:
            return ""

    # DOCX Parser
    elif ext in (".docx", ".doc"):
        try:
            import docx
            stream = io.BytesIO(content) if isinstance(content, (bytes, bytearray)) else content
            doc = docx.Document(stream)
            paragraphs = [p.text.strip() for p in doc.paragraphs if p.text.strip()]
            for table in doc.tables:
                for row in table.rows:
                    row_texts = [cell.text.strip() for cell in row.cells if cell.text.strip()]
                    if row_texts:
                        paragraphs.append(" | ".join(row_texts))
            return "\n".join(paragraphs)
        except Exception:
            return ""

    # TXT Parser
    else:
        if isinstance(content, str):
            return content
        data = content if isinstance(content, (bytes, bytearray)) else content.read()
        for encoding in ("utf-8", "latin-1", "cp1252", "utf-16"):
            try:
                return data.decode(encoding)
            except UnicodeDecodeError:
                continue
        return data.decode("utf-8", errors="replace")


# ==============================================================================
# 3. TF-IDF & COSINE SIMILARITY ENGINE
# ==============================================================================

class SimilarityEngine:
    """Computes TF-IDF vectorization and Cosine Similarity."""

    def __init__(self, min_df: int = 1, ngram_range: Tuple[int, int] = (1, 2)):
        self.ngram_range = ngram_range
        self.min_df = min_df

    def compute_similarities(self, job_description: str, resumes: List[str]) -> List[float]:
        if not resumes:
            return []

        cleaned_jd = clean_text(job_description)
        cleaned_resumes = [clean_text(r) for r in resumes]
        corpus = [cleaned_jd] + cleaned_resumes

        if not any(doc.strip() for doc in corpus):
            return [0.0] * len(resumes)

        vectorizer = TfidfVectorizer(
            ngram_range=self.ngram_range,
            stop_words=list(STOPWORDS),
            min_df=self.min_df,
            sublinear_tf=True,
            norm="l2"
        )

        try:
            tfidf_matrix = vectorizer.fit_transform(corpus)
        except ValueError:
            vectorizer = TfidfVectorizer(ngram_range=(1, 1), sublinear_tf=True, norm="l2")
            tfidf_matrix = vectorizer.fit_transform(corpus)

        jd_vector = tfidf_matrix[0:1]
        resume_vectors = tfidf_matrix[1:]

        cosine_sims = cosine_similarity(resume_vectors, jd_vector).flatten()
        return [float(np.clip(score, 0.0, 1.0)) for score in cosine_sims]


# ==============================================================================
# 4. CANDIDATE RANKING ALGORITHM
# ==============================================================================

class CandidateRanker:
    """Ranks candidates using composite multi-factor scoring and skill gap analysis."""

    def __init__(self, weight_similarity: float = 0.40, weight_skills: float = 0.45, weight_experience: float = 0.15):
        total = weight_similarity + weight_skills + weight_experience
        if total <= 0:
            total = 1.0
        self.w_sim = weight_similarity / total
        self.w_skill = weight_skills / total
        self.w_exp = weight_experience / total
        self.similarity_engine = SimilarityEngine()

    def rank_candidates(self, job_description: str, resumes: List[Dict[str, Any]]) -> Dict[str, Any]:
        if not resumes:
            return {
                "job_analysis": {"skills": [], "required_experience_years": 0.0},
                "ranked_candidates": [],
                "summary_metrics": {"total_candidates": 0, "avg_score": 0.0, "top_score": 0.0}
            }

        jd_skills_data = extract_skills(job_description)
        jd_skills_set = set(jd_skills_data["skills"])
        jd_exp_req = extract_experience_years(job_description)

        resume_texts = [r.get("text", "") for r in resumes]
        similarity_scores = self.similarity_engine.compute_similarities(job_description, resume_texts)

        evaluated_candidates = []

        for idx, resume_item in enumerate(resumes):
            raw_text = resume_item.get("text", "")
            filename = resume_item.get("filename", f"Resume_{idx+1}")
            cid = resume_item.get("id", str(idx + 1))

            cand_skills_data = extract_skills(raw_text)
            cand_skills_set = set(cand_skills_data["skills"])
            
            contact = extract_contact_info(raw_text)
            name = extract_candidate_name(raw_text, filename=filename)
            exp_years = extract_experience_years(raw_text)
            education = extract_education(raw_text)

            matched_skills = sorted(list(jd_skills_set.intersection(cand_skills_set)))
            missing_skills = sorted(list(jd_skills_set.difference(cand_skills_set)))
            additional_skills = sorted(list(cand_skills_set.difference(jd_skills_set)))

            if jd_skills_set:
                skill_ratio = len(matched_skills) / len(jd_skills_set)
                bonus = min(len(additional_skills) * 0.01, 0.10)
                skill_score = min(skill_ratio + bonus, 1.0)
            else:
                skill_score = similarity_scores[idx]

            if jd_exp_req > 0:
                if exp_years >= jd_exp_req:
                    exp_score = 1.0
                elif exp_years > 0:
                    exp_score = max(0.2, exp_years / jd_exp_req)
                else:
                    exp_score = 0.3
            else:
                exp_score = 1.0 if exp_years >= 2.0 else 0.8

            tfidf_score = similarity_scores[idx]

            composite_score = (
                (self.w_sim * tfidf_score) +
                (self.w_skill * skill_score) +
                (self.w_exp * exp_score)
            ) * 100.0
            
            final_score = round(float(composite_score), 1)

            if final_score >= 75.0:
                tier, tier_color = "Strong Match", "emerald"
            elif final_score >= 50.0:
                tier, tier_color = "Moderate Match", "amber"
            else:
                tier, tier_color = "Low Match", "rose"

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
                },
                "snippet": raw_text[:400].strip() + ("..." if len(raw_text) > 400 else "")
            })

        ranked_candidates = sorted(evaluated_candidates, key=lambda c: c["score"], reverse=True)
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


# ==============================================================================
# 5. PRE-LOADED DEMO ROLES & CANDIDATES
# ==============================================================================

SAMPLE_JOB_DESCRIPTIONS = [
    {
        "id": "jd-fullstack",
        "title": "Senior Full-Stack Engineer",
        "description": """Job Title: Senior Full-Stack Engineer
Experience: 4+ years of professional software engineering experience
Requirements: React, TypeScript, Next.js, Node.js, FastAPI, PostgreSQL, Docker, AWS, GraphQL, Redis, CI/CD pipelines.
Responsibilities: Build modern user interfaces and high-throughput APIs."""
    },
    {
        "id": "jd-ml",
        "title": "Machine Learning & NLP Engineer",
        "description": """Job Title: Machine Learning & NLP Engineer
Experience: 3+ years in Applied ML / NLP
Requirements: Python, PyTorch, TensorFlow, Scikit-Learn, NLP, Large Language Models (LLMs), LangChain, Transformers, Docker, FastAPI."""
    },
    {
        "id": "jd-devops",
        "title": "DevOps & Cloud Engineer",
        "description": """Job Title: DevOps & Cloud Infrastructure Engineer
Experience: 5+ years experience
Requirements: AWS, Kubernetes, Docker, Terraform, Ansible, CI/CD, Linux, Python, Prometheus, Grafana, Microservices."""
    }
]

SAMPLE_RESUMES = [
    {
        "id": "cand-alex",
        "filename": "Alex_Rivera_FullStack.txt",
        "text": """Alex Rivera
Email: alex.rivera.dev@gmail.com | Phone: (415) 555-0192 | San Francisco, CA
Summary: Senior Full-Stack Engineer with 5+ years experience. Expert in React, TypeScript, Next.js, Node.js, FastAPI, PostgreSQL, Docker, AWS, GraphQL, and Redis.
Education: Bachelor of Science in Computer Science"""
    },
    {
        "id": "cand-elena",
        "filename": "Dr_Elena_Rostova_AI_NLP.txt",
        "text": """Dr. Elena Rostova, Ph.D.
Email: elena.rostova.ai@outlook.com | Phone: (617) 555-0148 | Boston, MA
Summary: Lead AI & NLP Research Engineer with 6+ years experience in Natural Language Processing, PyTorch, Scikit-Learn, Transformers, Large Language Models (LLMs), LangChain, and Docker.
Education: Ph.D. in Computer Science from MIT"""
    },
    {
        "id": "cand-marcus",
        "filename": "Marcus_Chen_DevOps.txt",
        "text": """Marcus Chen
Email: marcus.chen.infra@gmail.com | Phone: (206) 555-0183 | Seattle, WA
Summary: DevOps & Cloud Architect with 7+ years experience. Deep expertise in AWS, Kubernetes, Docker, Terraform, Ansible, CI/CD, Linux, and Prometheus.
Education: Master of Science in Electrical Engineering"""
    },
    {
        "id": "cand-priya",
        "filename": "Priya_Sharma_Software_Dev.txt",
        "text": """Priya Sharma
Email: priya.sharma.codes@gmail.com | Phone: (312) 555-0177 | Chicago, IL
Summary: Mid-level Software Developer with 2.5 years experience in Python, Django, React, JavaScript, MySQL, Docker, and Git.
Education: Bachelor of Science in Information Technology"""
    },
    {
        "id": "cand-jordan",
        "filename": "Jordan_Taylor_Junior.txt",
        "text": """Jordan Taylor
Email: jordan.taylor.web@gmail.com | Phone: (602) 555-0112 | Phoenix, AZ
Summary: Junior Web Intern with 1 year experience building basic websites using HTML/CSS, Bootstrap, and basic JavaScript.
Education: Associate Degree in Web Technologies"""
    }
]


# ==============================================================================
# 6. FASTAPI REST API ENDPOINTS
# ==============================================================================

app = FastAPI(title="TalentMatch AI - All-in-One Resume Screener")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return {"status": "healthy", "version": "1.0.0"}


@app.get("/api/samples")
def get_samples():
    return {
        "job_descriptions": SAMPLE_JOB_DESCRIPTIONS,
        "resumes": [{"id": r["id"], "filename": r["filename"]} for r in SAMPLE_RESUMES]
    }


@app.post("/api/analyze-jd")
async def analyze_jd(job_description: Optional[str] = Form(None), job_file: Optional[UploadFile] = File(None)):
    text = ""
    if job_file and job_file.filename:
        content = await job_file.read()
        text = extract_document_text(job_file.filename, content)
    elif job_description:
        text = job_description

    skills_data = extract_skills(text)
    exp = extract_experience_years(text)
    return {
        "skills": skills_data["skills"],
        "categories": skills_data["categories"],
        "required_experience_years": exp
    }


@app.post("/api/rank")
async def rank_resumes_api(
    job_description: Optional[str] = Form(None),
    job_file: Optional[UploadFile] = File(None),
    resumes: List[UploadFile] = File(...),
    weight_similarity: float = Form(0.40),
    weight_skills: float = Form(0.45),
    weight_experience: float = Form(0.15)
):
    jd_text = ""
    if job_file and job_file.filename:
        content = await job_file.read()
        jd_text = extract_document_text(job_file.filename, content)
    elif job_description:
        jd_text = job_description

    if not jd_text.strip():
        raise HTTPException(status_code=400, detail="Job description is required.")

    parsed = []
    for idx, f in enumerate(resumes):
        if not f.filename:
            continue
        try:
            content = await f.read()
            extracted = extract_document_text(f.filename, content)
            if extracted.strip():
                parsed.append({"id": f"upload-{idx+1}", "filename": f.filename, "text": extracted})
        except Exception:
            continue

    if not parsed:
        raise HTTPException(status_code=400, detail="Could not parse any resume files.")

    ranker = CandidateRanker(weight_similarity, weight_skills, weight_experience)
    result = ranker.rank_candidates(jd_text, parsed)
    return {"success": True, **result}


@app.post("/api/rank-samples")
def rank_samples_api(
    sample_jd_id: str = Form("jd-fullstack"),
    weight_similarity: float = Form(0.40),
    weight_skills: float = Form(0.45),
    weight_experience: float = Form(0.15)
):
    selected_jd = next((jd for jd in SAMPLE_JOB_DESCRIPTIONS if jd["id"] == sample_jd_id), SAMPLE_JOB_DESCRIPTIONS[0])
    ranker = CandidateRanker(weight_similarity, weight_skills, weight_experience)
    result = ranker.rank_candidates(selected_jd["description"], SAMPLE_RESUMES)
    return {"success": True, **result}


# ==============================================================================
# 7. EMBEDDED COMPLETE FRONTEND UI (SERVED AT ROOT "/")
# ==============================================================================

HTML_UI = """
<!DOCTYPE html>
<html lang="en" class="dark">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>TalentMatch AI - Resume Screening & Candidate Ranking</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <script src="https://unpkg.com/lucide@latest"></script>
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');
    body { font-family: 'Inter', sans-serif; background: #090d16; color: #f1f5f9; }
    .glass-panel { background: rgba(17, 24, 39, 0.75); backdrop-filter: blur(16px); border: 1px solid rgba(255, 255, 255, 0.08); }
    .drop-zone { border: 2px dashed rgba(99, 102, 241, 0.35); transition: all 0.2s; background: rgba(15, 23, 42, 0.5); }
    .drop-zone.dragover { border-color: #6366f1; background: rgba(99, 102, 241, 0.12); }
  </style>
</head>
<body class="min-h-screen flex flex-col">

  <!-- Header -->
  <header class="border-b border-slate-800 bg-slate-900/80 backdrop-blur-md sticky top-0 z-40">
    <div class="max-w-7xl mx-auto px-4 h-16 flex items-center justify-between">
      <div class="flex items-center gap-3">
        <div class="w-9 h-9 rounded-xl bg-indigo-600 flex items-center justify-center text-white shadow-lg">
          <i data-lucide="sparkles" class="w-5 h-5"></i>
        </div>
        <div>
          <span class="text-lg font-extrabold bg-gradient-to-r from-white to-indigo-300 bg-clip-text text-transparent">
            TalentMatch AI
          </span>
          <span class="text-[11px] ml-2 px-2 py-0.5 rounded-full bg-indigo-500/10 text-indigo-400 border border-indigo-500/20">
            NLP + TF-IDF Ranker
          </span>
        </div>
      </div>
      <div class="text-xs text-emerald-400 bg-emerald-500/10 px-3 py-1 rounded-full border border-emerald-500/20 flex items-center gap-1.5">
        <span class="w-2 h-2 rounded-full bg-emerald-400 animate-ping"></span> Live Engine Ready
      </div>
    </div>
  </header>

  <!-- Main Grid -->
  <main class="flex-1 max-w-7xl w-full mx-auto px-4 py-8 grid grid-cols-1 lg:grid-cols-12 gap-8">
    
    <!-- LEFT COLUMN -->
    <section class="lg:col-span-5 space-y-6">
      
      <!-- JD Card -->
      <div class="glass-panel rounded-2xl p-5 border border-slate-800">
        <div class="flex items-center justify-between mb-3">
          <h2 class="text-sm font-semibold text-white flex items-center gap-2">
            <i data-lucide="briefcase" class="w-4 h-4 text-indigo-400"></i> Target Job Description
          </h2>
          <span class="text-xs text-indigo-400 font-mono" id="jd-exp">Exp: Auto</span>
        </div>
        
        <div class="flex gap-1.5 mb-3" id="jd-presets">
          <button data-id="jd-fullstack" class="px-2.5 py-1 text-xs rounded-lg bg-indigo-600 text-white font-medium">Full-Stack</button>
          <button data-id="jd-ml" class="px-2.5 py-1 text-xs rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300">ML / NLP</button>
          <button data-id="jd-devops" class="px-2.5 py-1 text-xs rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300">DevOps</button>
        </div>

        <textarea id="jd-text" rows="5" class="w-full text-xs font-mono bg-slate-900 border border-slate-700 rounded-xl p-3 text-slate-200 focus:ring-2 focus:ring-indigo-500 outline-none"></textarea>
        
        <div class="mt-3 pt-3 border-t border-slate-800">
          <span class="text-[11px] text-slate-400 font-semibold block mb-1.5">Detected JD Skills:</span>
          <div id="jd-skills-box" class="flex flex-wrap gap-1 max-h-20 overflow-y-auto"></div>
        </div>
      </div>

      <!-- Resumes Card -->
      <div class="glass-panel rounded-2xl p-5 border border-slate-800">
        <div class="flex items-center justify-between mb-3">
          <h2 class="text-sm font-semibold text-white flex items-center gap-2">
            <i data-lucide="file-up" class="w-4 h-4 text-indigo-400"></i> Candidate Resumes
          </h2>
          <button id="btn-load-demo" class="text-xs px-2.5 py-1 rounded-lg bg-emerald-500/10 text-emerald-400 border border-emerald-500/30 hover:bg-emerald-500/20">
            Load 5 Demo Resumes
          </button>
        </div>

        <div id="drop-box" class="drop-zone rounded-xl p-6 text-center cursor-pointer relative">
          <input type="file" id="file-input" multiple accept=".pdf,.docx,.txt" class="absolute inset-0 opacity-0 cursor-pointer">
          <i data-lucide="upload-cloud" class="w-8 h-8 text-indigo-400 mx-auto mb-1"></i>
          <p class="text-xs text-slate-300">Drag & drop files or <span class="text-indigo-400 font-semibold">browse</span></p>
          <p class="text-[10px] text-slate-500 mt-1">PDF, DOCX, TXT</p>
        </div>

        <div id="file-queue" class="mt-3 space-y-1 max-h-32 overflow-y-auto hidden"></div>
      </div>

      <!-- Weights Sliders -->
      <div class="glass-panel rounded-2xl p-4 border border-slate-800 text-xs space-y-2.5">
        <div class="flex justify-between text-slate-300 font-semibold">
          <span>Scoring Weights:</span>
        </div>
        <div>
          <div class="flex justify-between mb-1"><span>TF-IDF Similarity</span><span id="w-sim-lbl" class="text-indigo-400">40%</span></div>
          <input type="range" id="w-sim" min="0" max="100" value="40" class="w-full accent-indigo-500">
        </div>
        <div>
          <div class="flex justify-between mb-1"><span>Skill Match Ratio</span><span id="w-skill-lbl" class="text-indigo-400">45%</span></div>
          <input type="range" id="w-skill" min="0" max="100" value="45" class="w-full accent-indigo-500">
        </div>
        <div>
          <div class="flex justify-between mb-1"><span>Experience Fit</span><span id="w-exp-lbl" class="text-indigo-400">15%</span></div>
          <input type="range" id="w-exp" min="0" max="100" value="15" class="w-full accent-indigo-500">
        </div>
      </div>

      <button id="btn-rank" class="w-full py-3.5 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white font-semibold flex items-center justify-center gap-2 shadow-lg shadow-indigo-600/30">
        <i data-lucide="zap" class="w-4 h-4"></i> Analyze & Rank Candidates
      </button>

    </section>

    <!-- RIGHT COLUMN: RESULTS -->
    <section class="lg:col-span-7 space-y-5">
      
      <!-- Metrics Strip -->
      <div class="grid grid-cols-4 gap-3 text-center">
        <div class="glass-panel p-3 rounded-xl"><span class="text-[10px] text-slate-400 uppercase block">Screened</span><span id="m-total" class="text-xl font-bold text-white">0</span></div>
        <div class="glass-panel p-3 rounded-xl"><span class="text-[10px] text-slate-400 uppercase block">Top Score</span><span id="m-top" class="text-xl font-bold text-emerald-400">--</span></div>
        <div class="glass-panel p-3 rounded-xl"><span class="text-[10px] text-slate-400 uppercase block">Avg Score</span><span id="m-avg" class="text-xl font-bold text-indigo-400">--</span></div>
        <div class="glass-panel p-3 rounded-xl"><span class="text-[10px] text-slate-400 uppercase block">Strong</span><span id="m-strong" class="text-xl font-bold text-emerald-400">0</span></div>
      </div>

      <!-- Leaderboard -->
      <div class="glass-panel rounded-2xl p-5 border border-slate-800">
        <div class="flex items-center justify-between mb-4">
          <h2 class="text-sm font-semibold text-white flex items-center gap-2">
            <i data-lucide="award" class="w-4 h-4 text-indigo-400"></i> Candidate Leaderboard
          </h2>
          <button id="btn-csv" disabled class="text-xs px-2.5 py-1 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 border border-slate-700 disabled:opacity-40">
            Export CSV
          </button>
        </div>

        <div id="results-empty" class="py-16 text-center text-slate-500 text-xs">
          Select a role, load demo candidates, and click "Analyze & Rank Candidates".
        </div>

        <div id="results-list" class="space-y-3 hidden"></div>
      </div>

    </section>

  </main>

  <script>
    let samples = null;
    let selectedJdId = "jd-fullstack";
    let myFiles = [];
    let isDemo = true;
    let rankOutput = null;

    document.addEventListener("DOMContentLoaded", async () => {
      lucide.createIcons();
      const res = await fetch("/api/samples");
      samples = await res.json();
      loadPreset(selectedJdId);

      // Presets
      document.getElementById("jd-presets").addEventListener("click", (e) => {
        if (e.target.dataset.id) {
          selectedJdId = e.target.dataset.id;
          document.querySelectorAll("#jd-presets button").forEach(b => {
            b.className = b.dataset.id === selectedJdId ? "px-2.5 py-1 text-xs rounded-lg bg-indigo-600 text-white font-medium" : "px-2.5 py-1 text-xs rounded-lg bg-slate-800 text-slate-300";
          });
          loadPreset(selectedJdId);
        }
      });

      // Sliders
      const sim = document.getElementById("w-sim");
      const skl = document.getElementById("w-skill");
      const exp = document.getElementById("w-exp");
      sim.oninput = () => document.getElementById("w-sim-lbl").innerText = sim.value + "%";
      skl.oninput = () => document.getElementById("w-skill-lbl").innerText = skl.value + "%";
      exp.oninput = () => document.getElementById("w-exp-lbl").innerText = exp.value + "%";

      // File input
      const fileInput = document.getElementById("file-input");
      fileInput.onchange = (e) => {
        isDemo = false;
        myFiles = [...myFiles, ...e.target.files];
        renderQueue();
      };

      document.getElementById("btn-load-demo").onclick = () => {
        isDemo = true;
        myFiles = [];
        const q = document.getElementById("file-queue");
        q.className = "mt-3 space-y-1 block";
        q.innerHTML = '<div class="p-2 rounded bg-emerald-500/10 border border-emerald-500/20 text-xs text-emerald-400">5 Demo Resumes Active</div>';
      };

      // Rank CTA
      document.getElementById("btn-rank").onclick = async () => {
        const jd = document.getElementById("jd-text").value.trim();
        const fd = new FormData();
        fd.append("weight_similarity", sim.value / 100);
        fd.append("weight_skills", skl.value / 100);
        fd.append("weight_experience", exp.value / 100);

        let res;
        if (isDemo && myFiles.length === 0) {
          fd.append("sample_jd_id", selectedJdId);
          res = await fetch("/api/rank-samples", { method: "POST", body: fd });
        } else {
          fd.append("job_description", jd);
          myFiles.forEach(f => fd.append("resumes", f));
          res = await fetch("/api/rank", { method: "POST", body: fd });
        }

        rankOutput = await res.json();
        renderResults(rankOutput);
      };

      // CSV Export
      document.getElementById("btn-csv").onclick = () => {
        if (!rankOutput) return;
        const rows = [["Rank", "Name", "Score", "Matched Skills", "Missing Skills"]];
        rankOutput.ranked_candidates.forEach(c => rows.push([c.rank, `"${c.name}"`, c.score, `"${c.matched_skills.join(', ')}"`, `"${c.missing_skills.join(', ')}"`]));
        const csv = "data:text/csv;charset=utf-8," + rows.map(r => r.join(",")).join("\\n");
        const a = document.createElement("a");
        a.href = encodeURI(csv);
        a.download = "Candidate_Rankings.csv";
        a.click();
      };
    });

    function loadPreset(id) {
      if (!samples) return;
      const jd = samples.job_descriptions.find(j => j.id === id);
      if (jd) {
        document.getElementById("jd-text").value = jd.description.trim();
        analyze(jd.description);
      }
    }

    async function analyze(text) {
      const fd = new FormData();
      fd.append("job_description", text);
      const res = await fetch("/api/analyze-jd", { method: "POST", body: fd });
      const data = await res.json();
      document.getElementById("jd-exp").innerText = data.required_experience_years > 0 ? `${data.required_experience_years}+ yrs req` : "Exp: Open";
      const box = document.getElementById("jd-skills-box");
      box.innerHTML = data.skills.map(s => `<span class="px-1.5 py-0.5 text-[10px] rounded bg-slate-800 text-indigo-300 border border-slate-700">${s}</span>`).join("");
    }

    function renderQueue() {
      const q = document.getElementById("file-queue");
      q.className = "mt-3 space-y-1 block";
      q.innerHTML = myFiles.map(f => `<div class="text-xs bg-slate-900 p-1.5 rounded text-slate-300">${f.name}</div>`).join("");
    }

    function renderResults(data) {
      document.getElementById("results-empty").classList.add("hidden");
      const list = document.getElementById("results-list");
      list.classList.remove("hidden");
      document.getElementById("btn-csv").disabled = false;

      document.getElementById("m-total").innerText = data.summary_metrics.total_candidates;
      document.getElementById("m-top").innerText = data.summary_metrics.top_score + "%";
      document.getElementById("m-avg").innerText = data.summary_metrics.avg_score + "%";
      document.getElementById("m-strong").innerText = data.summary_metrics.strong_matches;

      list.innerHTML = data.ranked_candidates.map(c => `
        <div class="glass-panel p-4 rounded-xl border border-slate-800 text-xs">
          <div class="flex justify-between items-center mb-2">
            <div class="flex items-center gap-2">
              <span class="w-6 h-6 rounded bg-slate-800 font-bold flex items-center justify-center text-slate-300">#${c.rank}</span>
              <span class="font-bold text-white text-sm">${c.name}</span>
              <span class="text-slate-400">(${c.experience_years > 0 ? c.experience_years + ' yrs' : 'Exp detected'})</span>
            </div>
            <span class="px-2 py-0.5 rounded-full font-bold ${c.score >= 75 ? 'bg-emerald-500/10 text-emerald-400' : (c.score >= 50 ? 'bg-amber-500/10 text-amber-400' : 'bg-rose-500/10 text-rose-400')}">
              ${c.score}% Match
            </span>
          </div>
          <div class="w-full bg-slate-900 h-1.5 rounded-full mb-2.5">
            <div class="h-1.5 rounded-full ${c.score >= 75 ? 'bg-emerald-500' : (c.score >= 50 ? 'bg-amber-500' : 'bg-rose-500')}" style="width: ${c.score}%"></div>
          </div>
          <div class="space-y-1">
            <div><span class="text-emerald-400 font-semibold">Matched:</span> ${c.matched_skills.map(s => `<span class="inline-block px-1.5 py-0.5 rounded bg-emerald-950 text-emerald-300 text-[10px] mr-1">${s}</span>`).join("") || 'None'}</div>
            <div><span class="text-rose-400 font-semibold">Missing:</span> ${c.missing_skills.map(s => `<span class="inline-block px-1.5 py-0.5 rounded bg-rose-950 text-rose-300 text-[10px] mr-1">${s}</span>`).join("") || 'None'}</div>
          </div>
        </div>
      `).join("");
      lucide.createIcons();
    }
  </script>
</body>
</html>
"""


@app.get("/", response_class=HTMLResponse)
def serve_ui():
    """Serve the complete embedded frontend dashboard."""
    return HTML_UI


# ==============================================================================
# 8. TERMINAL ENTRYPOINT WITH AUTO-BROWSER LAUNCH
# ==============================================================================

def open_browser_delayed():
    """Wait 1.5 seconds for server startup, then automatically open the browser."""
    time.sleep(1.5)
    try:
        webbrowser.open("http://127.0.0.1:8000")
    except Exception:
        pass


if __name__ == "__main__":
    print("\n" + "=" * 65)
    print(" [*] TALENTMATCH AI - RESUME SCREENING & CANDIDATE RANKING")
    print(" [*] Server URL:  http://127.0.0.1:8000")
    print(" [*] API Docs:    http://127.0.0.1:8000/docs")
    print(" [*] Opening browser automatically...")
    print("=" * 65 + "\n")

    # Launch browser in a background thread
    threading.Thread(target=open_browser_delayed, daemon=True).start()

    # Start FastAPI / Uvicorn server directly
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=False)
