"""
Main FastAPI Application Entrypoint
"""
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from apscheduler.schedulers.background import BackgroundScheduler

from app.models.database import init_db, SessionLocal
from app.services.sync_service import seed_sample_data_if_empty, sync_tally_data
from app.api.routes import router

app = FastAPI(
    title="TallyAI Remote Backend & Sync API",
    description="API for Tally Prime real-time synchronization, financial dashboards, and business intelligence.",
    version="1.0.0"
)

# Enable CORS for remote access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

# Mount frontend if built (for Dokploy all-in-one container)
frontend_dist = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "frontend", "dist"))
if os.path.exists(frontend_dist):
    app.mount("/assets", StaticFiles(directory=os.path.join(frontend_dist, "assets")), name="assets")

    @app.get("/")
    def serve_frontend_root():
        return FileResponse(os.path.join(frontend_dist, "index.html"))

    @app.get("/{catchall:path}")
    def serve_frontend_spa(catchall: str):
        file_path = os.path.join(frontend_dist, catchall)
        if os.path.isfile(file_path):
            return FileResponse(file_path)
        return FileResponse(os.path.join(frontend_dist, "index.html"))
else:
    @app.get("/")
    def root():
        return {
            "service": "TallyAI Remote Server",
            "status": "online",
            "docs_url": "/docs",
            "api_prefix": "/api/v1"
        }
