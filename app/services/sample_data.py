"""Pre-built sample Job Descriptions and Candidate Resumes for instant testing."""

from typing import List, Dict, Any

SAMPLE_JOB_DESCRIPTIONS: List[Dict[str, Any]] = [
    {
        "id": "jd-fullstack",
        "title": "Senior Full-Stack Engineer",
        "department": "Engineering",
        "required_experience": "4+ years",
        "description": """
Job Title: Senior Full-Stack Engineer
Location: Remote / Hybrid
Experience Required: 4+ years of professional software engineering experience

About the Role:
We are seeking an experienced Senior Full-Stack Engineer to design and build scalable, high-performance web applications. You will collaborate with cross-functional teams to architect intuitive frontend experiences and robust backend APIs.

Key Responsibilities:
- Build responsive, modern user interfaces using React, TypeScript, Next.js, and Tailwind CSS.
- Architect high-throughput RESTful APIs and GraphQL services with Node.js and FastAPI / Python.
- Model and optimize relational databases using PostgreSQL and Redis caching.
- Deploy and orchestrate containerized microservices on AWS using Docker, Kubernetes, and CI/CD pipelines.
- Write thorough automated unit tests with Jest and PyTest, participating in code reviews and mentoring junior engineers.

Requirements & Skills:
- 4+ years of software development experience with modern JavaScript / TypeScript and Python.
- Strong proficiency in React, Next.js, and state management (Redux).
- Proven expertise in backend development with Node.js, Express.js, or FastAPI.
- Solid experience with PostgreSQL, SQL schema design, and Redis.
- Hands-on experience with Docker, AWS cloud services (S3, EC2, ECS), and GitHub Actions CI/CD.
- Excellent problem-solving, system design, and communication skills.
- Bachelor's degree in Computer Science, Software Engineering, or equivalent experience.
"""
    },
    {
        "id": "jd-ml",
        "title": "Machine Learning & NLP Engineer",
        "department": "Artificial Intelligence",
        "required_experience": "3+ years",
        "description": """
Job Title: Machine Learning & NLP Engineer
Location: San Francisco, CA / Remote
Experience Required: 3+ years in Applied ML / NLP

About the Role:
Join our AI Innovation Lab building state-of-the-art Natural Language Processing pipelines and Generative AI applications. You will work on fine-tuning Large Language Models (LLMs), developing RAG architectures, and deploying production machine learning models.

Key Responsibilities:
- Develop, train, and evaluate machine learning models for document analysis, sentiment analysis, and entity extraction using PyTorch and Scikit-Learn.
- Build LLM applications utilizing LangChain, Hugging Face Transformers, and vector databases.
- Perform exploratory data analysis and feature engineering on massive unstructured text corpora with Pandas and NumPy.
- Package and deploy scalable ML inference endpoints using FastAPI, Docker, and Kubernetes.
- Implement automated model evaluation, monitoring, and continuous retraining pipelines.

Requirements & Skills:
- 3+ years of hands-on experience in Machine Learning, Deep Learning, and Natural Language Processing (NLP).
- Expert proficiency in Python and scientific computing libraries (NumPy, Pandas, Scikit-Learn).
- Solid experience with Deep Learning frameworks, primarily PyTorch or TensorFlow.
- Experience with Large Language Models (LLMs), Transformers, LangChain, and prompt engineering.
- Experience with FastAPI, Docker, and cloud platforms (AWS or GCP).
- Strong foundation in statistical learning, linear algebra, and data preprocessing.
- Master's or Ph.D. in Computer Science, Data Science, or related quantitative field.
"""
    },
    {
        "id": "jd-devops",
        "title": "DevOps & Cloud Infrastructure Engineer",
        "department": "Infrastructure & Operations",
        "required_experience": "5+ years",
        "description": """
Job Title: DevOps & Cloud Infrastructure Engineer
Location: New York, NY / Remote
Experience Required: 5+ years of DevOps / Cloud engineering experience

About the Role:
We are looking for a seasoned DevOps & Cloud Infrastructure Engineer to scale our multi-region cloud architecture, strengthen security postures, and streamline continuous delivery.

Key Responsibilities:
- Design, implement, and maintain Infrastructure as Code (IaC) using Terraform on AWS.
- Manage containerized orchestration with Kubernetes (EKS) and Docker across development and production environments.
- Build resilient, automated CI/CD pipelines using GitHub Actions, GitLab CI, or Jenkins.
- Oversee system reliability, automated alerts, and telemetry with Prometheus, Grafana, and ELK stack.
- Write automation scripts in Python and Bash for operational tasks and deployment workflows.

Requirements & Skills:
- 5+ years in DevOps, Site Reliability Engineering (SRE), or Cloud Architecture.
- Deep expertise in AWS cloud services (VPC, IAM, EKS, RDS, S3, Route53).
- Mastery of Kubernetes, Helm charts, Docker, and container security.
- Advanced Infrastructure as Code experience with Terraform and Ansible.
- Strong scripting skills in Python and Bash/Shell on Linux environments.
- Experience setting up centralized monitoring, logging, and tracing with Prometheus and Grafana.
- Bachelor's degree in Computer Science, Information Technology, or relevant field.
"""
    }
]

SAMPLE_RESUMES: List[Dict[str, Any]] = [
    {
        "id": "cand-alex",
        "filename": "Alex_Rivera_FullStack_Resume.txt",
        "text": """
Alex Rivera
Email: alex.rivera.dev@gmail.com | Phone: (415) 555-0192 | San Francisco, CA
GitHub: github.com/alexrivera-dev | LinkedIn: linkedin.com/in/alexrivera

PROFESSIONAL SUMMARY
Senior Full-Stack Engineer with 5+ years of experience building high-performance web applications and distributed backend microservices. Proven track record in TypeScript, React, Next.js, Node.js, FastAPI, PostgreSQL, and AWS cloud deployments. Passionate about clean architecture, unit testing, and developer productivity.

EXPERIENCE

Senior Full-Stack Engineer | Nexus Tech Solutions | 2022 - Present (San Francisco, CA)
- Architected and delivered customer-facing dashboard using React, TypeScript, Next.js, and Tailwind CSS, increasing user engagement by 42%.
- Built RESTful APIs and GraphQL endpoints using Node.js, Express.js, and FastAPI (Python), handling over 8M daily requests.
- Designed relational database schemas in PostgreSQL with Redis caching layer, optimizing query performance by 65%.
- Implemented automated CI/CD deployment pipelines using GitHub Actions and Docker, reducing release cycle time from hours to minutes.
- Conducted regular code reviews, mentored 4 junior engineers, and maintained 90%+ unit testing coverage using Jest and PyTest.

Software Engineer | CloudSphere Inc. | 2019 - 2022 (Austin, TX)
- Developed responsive web interfaces with React, Redux, and Bootstrap for SaaS enterprise clients.
- Built backend microservices in Python (Django and Flask) and integrated AWS S3, EC2, and RDS.
- Managed containerization workflows with Docker and assisted in migration to Kubernetes.
- Collaborated in an Agile/Scrum environment with bi-weekly sprint planning and Jira management.

EDUCATION
Bachelor of Science in Computer Science | University of Texas at Austin (2015 - 2019)

TECHNICAL SKILLS
- Languages: JavaScript, TypeScript, Python, SQL, HTML5, CSS3, Bash
- Frontend: React, Next.js, Redux, Tailwind CSS, Bootstrap, Webpack
- Backend & APIs: Node.js, Express.js, FastAPI, RESTful API, GraphQL
- Databases: PostgreSQL, MySQL, Redis, MongoDB
- DevOps & Cloud: AWS, Docker, Kubernetes, CI/CD, GitHub Actions, Linux, Git
- Methodologies: Agile/Scrum, System Design, Unit Testing, TDD
"""
    },
    {
        "id": "cand-elena",
        "filename": "Dr_Elena_Rostova_AI_NLP_Resume.txt",
        "text": """
Dr. Elena Rostova, Ph.D.
Email: elena.rostova.ai@outlook.com | Phone: (617) 555-0148 | Boston, MA
Google Scholar: scholar.google.com/elena-rostova | GitHub: github.com/erostova-nlp

PROFESSIONAL SUMMARY
Lead AI & NLP Research Engineer with 6+ years of experience in Natural Language Processing, Deep Learning, and Large Language Models. Expert in fine-tuning Transformer models (BERT, GPT), developing Retrieval-Augmented Generation (RAG) pipelines with LangChain, and deploying production ML systems with PyTorch, FastAPI, and Docker.

EXPERIENCE

Lead Machine Learning Scientist | Cognition AI Labs | 2021 - Present (Boston, MA)
- Led a team of 5 data scientists developing domain-specific Large Language Model (LLM) agents and RAG systems using LangChain and Hugging Face Transformers.
- Trained and fine-tuned deep neural networks (PyTorch, TensorFlow) on multi-terabyte text datasets, boosting semantic parsing accuracy by 28%.
- Built feature engineering and automated preprocessing pipelines using Scikit-Learn, Pandas, and NumPy.
- Packaged ML inference microservices using FastAPI and Docker, orchestrating zero-downtime deployments on Kubernetes and AWS.
- Authored 4 peer-reviewed research papers in top NLP conferences on transfer learning and transformer attention mechanisms.

Senior NLP Engineer | DataVertex Systems | 2018 - 2021 (Cambridge, MA)
- Developed production named entity recognition (NER) and sentiment analysis classification models using PyTorch, Scikit-Learn, and Spacy.
- Engineered automated data preprocessing and exploratory data analysis (EDA) pipelines on distributed text corpora using Python and Spark.
- Collaborated with engineering teams to deploy RESTful API endpoints and integrated Redis for embedding vector caching.

EDUCATION
Ph.D. in Computer Science (Artificial Intelligence & NLP) | Massachusetts Institute of Technology (MIT) (2014 - 2018)
Master of Science in Data Science | Carnegie Mellon University (2012 - 2014)
Bachelor of Science in Mathematics & Computer Science (2008 - 2012)

TECHNICAL SKILLS
- Core: Python, R, SQL, C++, Bash
- AI & ML: Machine Learning, Deep Learning, Natural Language Processing (NLP), Large Language Models (LLMs), LangChain, Transformers, PyTorch, TensorFlow, Scikit-Learn, Hugging Face
- Data: Pandas, NumPy, Data Analysis, Data Preprocessing, Feature Engineering, Big Data, Spark
- Engineering: FastAPI, Docker, Kubernetes, AWS, Git, Linux, CI/CD, Unit Testing
"""
    },
    {
        "id": "cand-marcus",
        "filename": "Marcus_Chen_DevOps_Cloud_Resume.txt",
        "text": """
Marcus Chen
Email: marcus.chen.infra@gmail.com | Phone: (206) 555-0183 | Seattle, WA
LinkedIn: linkedin.com/in/marcus-chen-cloud

PROFESSIONAL SUMMARY
DevOps & Cloud Infrastructure Architect with 7+ years of experience designing secure, self-healing cloud ecosystems across AWS and GCP. Extensive mastery in Kubernetes, Docker, Terraform, CI/CD pipeline automation, and enterprise monitoring with Prometheus and Grafana.

EXPERIENCE

Lead DevOps Engineer | Apex Cloud Technologies | 2020 - Present (Seattle, WA)
- Architected multi-region AWS infrastructure managing 500+ microservices using Terraform, AWS EKS (Kubernetes), and Route53.
- Engineered unified continuous deployment pipelines utilizing GitHub Actions, GitLab CI, and Helm, eliminating manual release errors.
- Designed automated monitoring and alerting infrastructure using Prometheus, Grafana, and Datadog, reducing MTTR by 55%.
- Authored infrastructure automation scripts in Python and Bash for automated failover and backup strategies.
- Enforced zero-trust cloud security policies, IAM role governance, and SOC2 compliance automation.

Senior Systems & DevOps Engineer | StrataScale Solutions | 2017 - 2020 (Portland, OR)
- Managed production Kubernetes clusters and containerized legacy monolithic applications using Docker and Linux.
- Implemented Infrastructure as Code (IaC) templates using Terraform and Ansible across hybrid cloud environments.
- Optimized AWS cloud spend through autoscaling policies and reserved instance allocation, saving $320k annually.

EDUCATION
Master of Science in Electrical Engineering & Computer Systems | University of Washington (2015 - 2017)
Bachelor of Science in Information Technology | Oregon State University (2011 - 2015)

TECHNICAL SKILLS
- Cloud Platforms: AWS, Google Cloud (GCP), Microsoft Azure
- DevOps & Containers: Docker, Kubernetes, Helm, Terraform, Ansible, CI/CD, GitHub Actions, Jenkins
- Scripting & Code: Python, Bash/Shell, Go, SQL, Linux administration
- Observability: Prometheus, Grafana, ELK Stack, Datadog, CloudWatch
- Protocols & Architecture: System Design, Microservices, Nginx, RESTful API, Git/GitHub
"""
    },
    {
        "id": "cand-priya",
        "filename": "Priya_Sharma_Software_Dev_Resume.txt",
        "text": """
Priya Sharma
Email: priya.sharma.codes@gmail.com | Phone: (312) 555-0177 | Chicago, IL
GitHub: github.com/priyasharma-dev

PROFESSIONAL SUMMARY
Mid-level Software Developer with 2.5 years of professional experience building web applications, REST APIs, and database-driven tools. Proficient in Python, Django, JavaScript, React, MySQL, and Docker. Enthusiastic about collaborative problem solving and agile product delivery.

EXPERIENCE

Software Developer | InnovateWeb Studio | 2023 - Present (Chicago, IL)
- Developed and maintained responsive frontend web applications using React, JavaScript, HTML5, and CSS3.
- Built backend RESTful APIs with Python and Django framework, implementing authentication and permissions.
- Designed relational schemas and wrote optimized SQL queries for MySQL databases.
- Integrated automated tests with PyTest and Jest to ensure code quality.
- Containerized development environments using Docker and tracked version control via Git / GitHub.

Junior Web Developer | Apex Digital Agency | 2022 - 2023 (Chicago, IL)
- Created interactive client websites using HTML, CSS, JavaScript, and Bootstrap.
- Collaborated in Agile Scrum sprints, attending daily standups and sprint planning sessions.
- Resolved bug tickets and implemented feature requests under senior engineer supervision.

EDUCATION
Bachelor of Science in Information Technology | University of Illinois Chicago (2018 - 2022)

TECHNICAL SKILLS
- Languages: Python, JavaScript, SQL, HTML/CSS
- Frameworks: React, Django, Flask, Bootstrap
- Databases: MySQL, SQLite, PostgreSQL
- Tools: Docker, Git/GitHub, Unit Testing, Agile/Scrum, RESTful API
"""
    },
    {
        "id": "cand-jordan",
        "filename": "Jordan_Taylor_Junior_Web_Resume.txt",
        "text": """
Jordan Taylor
Email: jordan.taylor.web@gmail.com | Phone: (602) 555-0112 | Phoenix, AZ

PROFESSIONAL SUMMARY
Motivated Junior Web Development Intern with 1 year of hands-on experience building foundational websites, crafting responsive HTML/CSS designs, and utilizing basic JavaScript. Eager to grow software development skills within a fast-paced team.

EXPERIENCE

Web Development Intern | Desert Bloom Media | 2023 - 2024 (Phoenix, AZ)
- Built landing pages using HTML, CSS, Bootstrap, and basic JavaScript.
- Assisted in updating website content, fixing layout responsiveness, and debugging cross-browser issues.
- Used Git for version control and participated in daily team meetings.

Customer Support Associate | TechFirst Solutions | 2022 - 2023 (Phoenix, AZ)
- Provided technical customer support for web hosting clients and recorded support tickets in Jira.

EDUCATION
Associate of Science in Web Technologies | Phoenix Community College (2021 - 2023)

TECHNICAL SKILLS
- Web: HTML/CSS, JavaScript, Bootstrap
- Tools: Git, GitHub, VS Code
- Soft Skills: Communication, Teamwork, Problem Solving
"""
    }
]
