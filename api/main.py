"""Uvicorn entry point for the application."""

import uvicorn

from api.app import app
from api.core.config import settings

if __name__ == "__main__":
    uvicorn.run(
        "api.app:app",
        host=settings.host,
        port=settings.port,
        reload=settings.environment == "development",
    )
