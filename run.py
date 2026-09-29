import os
import uvicorn

if __name__ == "__main__":
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))

    print("\n" + "=" * 60)
    print("[*] Starting AI Resume Screening & Candidate Ranking System")
    print(f"[*] Server listening on: http://{host}:{port}")
    print(f"[*] API Documentation:   http://{host}:{port}/docs")
    print("=" * 60 + "\n")
    uvicorn.run("app.main:app", host=host, port=port, reload=False)
