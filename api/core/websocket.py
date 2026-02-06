"""WebSocket connection manager for real-time progress updates."""

from typing import Dict, Set
from fastapi import WebSocket
import json
import asyncio


class ConnectionManager:
    """Manages WebSocket connections for job progress updates."""

    def __init__(self):
        self.active_connections: Dict[str, Set[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, job_id: str):
        """Accept a WebSocket connection for a specific job."""
        await websocket.accept()
        if job_id not in self.active_connections:
            self.active_connections[job_id] = set()
        self.active_connections[job_id].add(websocket)

    def disconnect(self, websocket: WebSocket, job_id: str):
        """Remove a WebSocket connection."""
        if job_id in self.active_connections:
            self.active_connections[job_id].discard(websocket)
            if not self.active_connections[job_id]:
                del self.active_connections[job_id]

    async def send_progress(self, job_id: str, data: dict):
        """Send progress update to all connections for a job."""
        if job_id not in self.active_connections:
            return

        message = json.dumps(data)
        dead_connections = set()

        for connection in self.active_connections[job_id]:
            try:
                await connection.send_text(message)
            except Exception:
                dead_connections.add(connection)

        # Clean up dead connections
        for connection in dead_connections:
            self.active_connections[job_id].discard(connection)


# Global connection manager instance
manager = ConnectionManager()


# Progress step definitions
PROGRESS_STEPS = [
    {"step": 1, "step_name": "Validation", "progress": 0.2},
    {"step": 2, "step_name": "Analyse Pass 1", "progress": 0.4},
    {"step": 3, "step_name": "Analyse Pass 2 (Z-score)", "progress": 0.6},
    {"step": 4, "step_name": "Generation rapport", "progress": 0.8},
    {"step": 5, "step_name": "Termine", "progress": 1.0},
]


async def send_step_progress(
    job_id: str,
    step: int,
    anomalies_found: int = 0,
    status: str = "processing",
    download_url: str | None = None,
):
    """Send a progress update for a specific step."""
    step_info = PROGRESS_STEPS[step - 1] if step <= len(PROGRESS_STEPS) else PROGRESS_STEPS[-1]

    data = {
        **step_info,
        "anomalies_found": anomalies_found,
        "status": status,
    }

    if download_url:
        data["download_url"] = download_url

    await manager.send_progress(job_id, data)
