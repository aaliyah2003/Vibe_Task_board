"""
Replit entry point: serves both FastAPI backend and static frontend
"""
import os
from pathlib import Path
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

# Import backend routes
from backend.main import app as backend_app, tasks, completion_days

# Create main app
app = FastAPI(title="Fluid Task Board")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount backend API routes
app.mount("/api", backend_app)

# Serve frontend static files
frontend_dir = Path("frontend")
if frontend_dir.exists():
    app.mount("/static", StaticFiles(directory=str(frontend_dir)), name="static")

@app.get("/")
async def serve_frontend():
    """Serve the main frontend HTML file"""
    index_path = frontend_dir / "index.html"
    if index_path.exists():
        return FileResponse(str(index_path))
    return {"message": "Frontend not found. Make sure frontend/index.html exists."}

@app.get("/health")
async def health():
    return {"status": "ok", "message": "Task Board API is running"}

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)

