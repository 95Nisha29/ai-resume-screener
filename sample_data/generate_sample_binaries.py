"""Generate binary .docx and .pdf files for testing."""

import os
from docx import Document

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RESUMES_DIR = os.path.join(BASE_DIR, "resumes")

# Generate DOCX for Alex Rivera
doc = Document()
doc.add_heading("Alex Rivera", level=0)
doc.add_paragraph("Email: alex.rivera.dev@gmail.com | Phone: (415) 555-0192 | San Francisco, CA")
doc.add_paragraph("GitHub: github.com/alexrivera-dev | LinkedIn: linkedin.com/in/alexrivera")

doc.add_heading("Professional Summary", level=1)
doc.add_paragraph(
    "Senior Full-Stack Engineer with 5+ years of experience building high-performance web applications "
    "and distributed backend microservices. Proven track record in TypeScript, React, Next.js, Node.js, "
    "FastAPI, PostgreSQL, and AWS cloud deployments."
)

doc.add_heading("Work Experience", level=1)
p1 = doc.add_paragraph()
p1.add_run("Senior Full-Stack Engineer | Nexus Tech Solutions | 2022 - Present\n").bold = True
p1.add_run(
    "- Architected customer dashboard using React, TypeScript, Next.js, and Tailwind CSS.\n"
    "- Built RESTful APIs and GraphQL endpoints using Node.js, Express.js, and FastAPI (Python).\n"
    "- Designed relational schemas in PostgreSQL with Redis caching layer.\n"
    "- Deployed microservices using Docker, Kubernetes, and GitHub Actions CI/CD.\n"
)

p2 = doc.add_paragraph()
p2.add_run("Software Engineer | CloudSphere Inc. | 2019 - 2022\n").bold = True
p2.add_run(
    "- Developed web interfaces with React, Redux, and Bootstrap.\n"
    "- Built backend microservices in Python (Django, Flask) and integrated AWS S3, EC2.\n"
    "- Containerized apps with Docker in an Agile/Scrum team.\n"
)

doc.add_heading("Education", level=1)
doc.add_paragraph("Bachelor of Science in Computer Science | University of Texas at Austin (2015 - 2019)")

doc.add_heading("Skills", level=1)
doc.add_paragraph("React, TypeScript, Python, Node.js, FastAPI, Next.js, PostgreSQL, Docker, Kubernetes, AWS, GraphQL, Redis, Git, CI/CD")

docx_path = os.path.join(RESUMES_DIR, "Alex_Rivera_FullStack_Resume.docx")
doc.save(docx_path)
print(f"Generated DOCX: {docx_path}")

# Create a 100% valid PDF with exact cross-reference offsets
def create_valid_pdf(filename: str, title: str, text_lines: list):
    """Construct a clean, valid PDF-1.4 file with correct xref offsets."""
    body = []
    
    # 1. Catalog
    body.append(b"1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n")
    # 2. Pages
    body.append(b"2 0 obj\n<< /Type /Pages /Kids [3 0 R] /Count 1 >>\nendobj\n")
    # 3. Page
    body.append(b"3 0 obj\n<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Resources << /Font << /F1 4 0 R >> >> /Contents 5 0 R >>\nendobj\n")
    # 4. Font
    body.append(b"4 0 obj\n<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>\nendobj\n")

    # 5. Content Stream
    stream_parts = ["BT", "/F1 14 Tf", "50 720 Td", f"({title}) Tj", "/F1 10 Tf"]
    y_offset = -20
    for line in text_lines:
        safe_line = line.replace("(", "").replace(")", "").replace("\\", "")
        stream_parts.append(f"0 {y_offset} Td ({safe_line}) Tj")
        y_offset = -15
    stream_parts.append("ET")
    stream_bytes = "\n".join(stream_parts).encode("latin-1")

    obj5 = f"5 0 obj\n<< /Length {len(stream_bytes)} >>\nstream\n".encode("latin-1") + stream_bytes + b"\nendstream\nendobj\n"
    body.append(obj5)

    # Calculate offsets
    header = b"%PDF-1.4\n"
    offsets = [0]
    curr_offset = len(header)
    for obj in body:
        offsets.append(curr_offset)
        curr_offset += len(obj)

    xref_offset = curr_offset
    xref = [f"xref\n0 {len(offsets)}\n0000000000 65535 f \r\n".encode("ascii")]
    for off in offsets[1:]:
        xref.append(f"{off:010d} 00000 n \r\n".encode("ascii"))

    trailer = (
        f"trailer\n<< /Size {len(offsets)} /Root 1 0 R >>\n"
        f"startxref\n{xref_offset}\n%%EOF\n"
    ).encode("ascii")

    full_pdf = header + b"".join(body) + b"".join(xref) + trailer
    with open(filename, "wb") as f:
        f.write(full_pdf)

pdf_path = os.path.join(RESUMES_DIR, "Dr_Elena_Rostova_AI_NLP_Resume.pdf")
create_valid_pdf(
    pdf_path,
    "Dr. Elena Rostova, Ph.D. - AI & NLP Specialist",
    [
        "Email: elena.rostova.ai@outlook.com | Phone: 617-555-0148",
        "Summary: Lead AI and NLP Research Engineer with 6+ years experience.",
        "Skills: Python, PyTorch, TensorFlow, Scikit-Learn, NLP, Transformers, LLMs, LangChain, Docker, AWS",
        "Experience: Lead Machine Learning Scientist at Cognition AI Labs",
        "Fine-tuned Transformer models BERT and GPT using PyTorch and Scikit-Learn",
        "Preprocessed massive text datasets using Pandas and NumPy",
        "Education: Ph.D. in Computer Science from MIT"
    ]
)
print(f"Generated valid PDF: {pdf_path}")
