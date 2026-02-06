"""Baseline data models."""

from datetime import date
from pydantic import BaseModel, Field


class NodeStatistics(BaseModel):
    """Statistical data for a single node (Compte x Section)."""

    compte: str = Field(..., description="Compte general")
    section: str = Field(..., description="Section analytique")
    monthly_amounts: list[float] = Field(default_factory=list, description="Monthly amounts")
    mean: float = Field(0.0, description="Mean value")
    std: float = Field(0.0, description="Standard deviation")
    count: int = Field(0, description="Number of observations")
    min_amount: float = Field(0.0, description="Minimum observed")
    max_amount: float = Field(0.0, description="Maximum observed")


class Baseline(BaseModel):
    """Baseline file structure for statistical comparison."""

    version: str = Field("1.0", description="Baseline format version")
    generated: str = Field(..., description="Generation date (ISO 8601)")
    project: str = Field("Controlmyentries", description="Project identifier")
    period_start: str | None = Field(None, description="First month in baseline")
    period_end: str | None = Field(None, description="Last month in baseline")
    months_count: int = Field(0, description="Number of months in baseline")
    nodes: list[NodeStatistics] = Field(default_factory=list, description="Per-node statistics")

    class Config:
        json_schema_extra = {
            "example": {
                "version": "1.0",
                "generated": "2026-02-06",
                "project": "Controlmyentries",
                "period_start": "2025-01",
                "period_end": "2025-12",
                "months_count": 12,
                "nodes": [
                    {
                        "compte": "601000",
                        "section": "ADMIN",
                        "monthly_amounts": [1000, 1100, 1050, 980],
                        "mean": 1032.5,
                        "std": 50.8,
                        "count": 4,
                        "min_amount": 980,
                        "max_amount": 1100,
                    }
                ],
            }
        }


class BaselineGenerationRequest(BaseModel):
    """Request to generate a baseline from GL data."""

    pass  # File is sent as multipart


class BaselineGenerationResponse(BaseModel):
    """Response from baseline generation."""

    success: bool
    nodes_count: int
    months_count: int
    period_start: str
    period_end: str
    download_url: str
    message: str
