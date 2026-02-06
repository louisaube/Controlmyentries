"""FastAPI application factory."""

from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from api.routes import router

app = FastAPI(
    title="Controlmyentries",
    description="Budget Monitoring Anomaly Detection Tool",
    version="0.1.0",
)

# Include API routes
app.include_router(router, prefix="/api")

# Mount static files for frontend (after build)
static_path = Path(__file__).parent.parent / "static"
if static_path.exists() and any(static_path.iterdir()):
    app.mount("/", StaticFiles(directory=str(static_path), html=True), name="static")
