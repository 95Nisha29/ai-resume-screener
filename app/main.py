"""FastAPI Application Main Entrypoint."""

import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.api.routes import router as api_router

app = FastAPI(
    title="AI Resume Screening & Candidate Ranking System",
    description="NLP-powered resume screening, skill gap analysis, and candidate ranking engine.",
    version="1.0.0"
)

# Configure CORS (supports custom ALLOWED_ORIGINS env var for production)
allowed_origins_env = os.getenv("ALLOWED_ORIGINS", "*")
allowed_origins = [o.strip() for o in allowed_origins_env.split(",") if o.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API routes
app.include_router(api_router, prefix="/api")
app.include_router(api_router)  # allows /health to be accessed directly

# Mount static folder
static_dir = os.path.join(os.path.dirname(__file__), "static")
if not os.path.exists(static_dir):
    os.makedirs(static_dir, exist_ok=True)

app.mount("/static", StaticFiles(directory=static_dir), name="static")


@app.get("/")
async def root():
    """Serve the Recruiter Dashboard Single Page Application."""
    index_path = os.path.join(static_dir, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"message": "AI Resume Screening API is running. Access UI at /"}
