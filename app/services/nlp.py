"""NLP Preprocessing, Entity Extraction, and Domain Skill Taxonomy Service."""

import re
from typing import Dict, List, Set, Tuple, Optional

# Standard English Stopwords + Resume Boilerplate (alphanumeric only to align with vectorizers)
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
    # Resume-specific boilerplate words
    "resume", "curriculum", "vitae", "cv", "page", "phone", "email", "contact", "address", 
    "date", "year", "years", "month", "months", "responsible", "duties", "including", "work", 
    "experience", "summary", "profile", "objective", "skills", "skill", "education"
}

# Extensive Categorized Skill Taxonomy
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

# Flattened alias map for fast phrase lookups: lowercase_alias -> canonical_name
ALIAS_TO_CANONICAL: Dict[str, str] = {}
CANONICAL_TO_CATEGORY: Dict[str, str] = {}

for category, skill_map in SKILL_TAXONOMY.items():
    for canonical, aliases in skill_map.items():
        CANONICAL_TO_CATEGORY[canonical] = category
        for alias in aliases:
            ALIAS_TO_CANONICAL[alias.lower()] = canonical
        ALIAS_TO_CANONICAL[canonical.lower()] = canonical

# Sort aliases by length descending to match longest multi-word phrases first
SORTED_ALIASES = sorted(ALIAS_TO_CANONICAL.keys(), key=lambda s: len(s), reverse=True)


def clean_text(text: str) -> str:
    """Normalize and clean raw text while keeping meaningful words."""
    if not text:
        return ""
    # Convert to lowercase
    text = text.lower()
    # Normalize unicode whitespace
    text = re.sub(r"[\r\t\f\v]+", " ", text)
    # Remove URLs
    text = re.sub(r"https?://\S+|www\.\S+", " ", text)
    # Normalize special characters often in tech (C++, C#, .NET)
    text = re.sub(r"c\+\+", "cpp", text)
    text = re.sub(r"c\#", "csharp", text)
    text = re.sub(r"\.net\b", "dotnet", text)
    # Replace other punctuation with spaces except hyphens in words
    text = re.sub(r"[^\w\s\-]", " ", text)
    # Normalize hyphens
    text = re.sub(r"\s-\s", " ", text)
    # Collapse consecutive spaces
    text = re.sub(r"\s+", " ", text).strip()
    return text


def tokenize(text: str, remove_stopwords: bool = True) -> List[str]:
    """Tokenize cleaned text into words and remove stopwords."""
    cleaned = clean_text(text)
    tokens = re.findall(r"\b[a-zA-Z0-9_\-\.\#\+]{2,}\b", cleaned)
    if remove_stopwords:
        tokens = [t for t in tokens if t.lower() not in STOPWORDS]
    return tokens


def extract_skills(text: str) -> Dict[str, List[str]]:
    """
    Extract recognized skills from text using phrase and regex matching.
    Returns:
      {
        'skills': [list of canonical skill names],
        'categories': {category_name: [skills]}
      }
    """
    if not text:
        return {"skills": [], "categories": {}}

    text_lower = " " + clean_text(text) + " "
    found_canonicals: Set[str] = set()

    for alias in SORTED_ALIASES:
        # Regex boundary check for words / tech tokens
        # Protect special chars like +, #, .
        escaped_alias = re.escape(alias)
        pattern = rf"(?<![a-zA-Z0-9]){escaped_alias}(?![a-zA-Z0-9])"
        if re.search(pattern, text_lower):
            canonical = ALIAS_TO_CANONICAL[alias]
            found_canonicals.add(canonical)

    # Group by category
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
    
    # Common resume header words to skip
    skip_headers = {
        "resume", "curriculum vitae", "cv", "profile", "contact", "summary",
        "professional summary", "career objective", "experience", "work experience",
        "education", "skills", "technical skills", "projects", "personal info"
    }

    for line in lines[:8]:
        line_clean = line.strip()
        # Skip if contains email or phone
        if "@" in line_clean or re.search(r"\d{3,}", line_clean):
            continue
        # Skip if short or header
        if line_clean.lower() in skip_headers or len(line_clean) < 3 or len(line_clean) > 40:
            continue
        
        words = line_clean.split()
        # Clean words from punctuation like commas, dots, and parens
        cleaned_words = [re.sub(r"[,().]+", "", w).strip() for w in words]
        cleaned_words = [w for w in cleaned_words if w]
        # Filter out titles/suffixes
        name_words = [w for w in cleaned_words if w.lower() not in {"dr", "phd", "mr", "ms", "mrs", "prof", "md", "eng"}]
        if 2 <= len(name_words) <= 4 and all(w.isalpha() for w in name_words):
            return " ".join(name_words).title()

    # Fallback to filename if provided
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
    """Extract estimated years of experience using heuristics and regex patterns."""
    if not text:
        return 0.0

    text_lower = text.lower()
    
    # Direct mention patterns: "5+ years", "3 years of experience", "4.5 yrs", "3+ years required"
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

    # Year range detection (e.g. 2018 - 2024, 2020 - Present)
    year_ranges = re.findall(r"\b(200\d|201\d|202\d)\s*(?:-|to|–)\s*(200\d|201\d|202\d|present|current)\b", text_lower)
    total_span = 0.0
    current_year = 2026

    if year_ranges:
        intervals = []
        for start_str, end_str in year_ranges:
            try:
                start = int(start_str)
                end = current_year if end_str in ("present", "current") else int(end_str)
                if 1990 <= start <= end <= current_year:
                    intervals.append((start, end))
            except ValueError:
                continue

        if intervals:
            # Merge overlapping intervals
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
