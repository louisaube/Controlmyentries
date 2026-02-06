"""Analysis result models."""

from enum import Enum
from pydantic import BaseModel, Field


class AnomalyType(str, Enum):
    """Types of anomalies detected."""

    DISPARITION = "disparition"  # Node disappeared (was active, now absent)
    APPARITION = "apparition"  # New node appeared
    VARIATION = "variation"  # Brutal variation > 20%
    RECURRENCE = "recurrence"  # Broken recurrence pattern
    ZSCORE = "zscore"  # Statistical anomaly (|Z| > 2)


class AnomalySeverity(str, Enum):
    """Severity levels for anomalies."""

    HIGH = "high"  # |Z| > 3 or critical pattern break
    MEDIUM = "medium"  # 2 < |Z| <= 3
    LOW = "low"  # Informational or borderline


class Anomaly(BaseModel):
    """A detected anomaly."""

    id: str = Field(..., description="Unique anomaly identifier")
    type: AnomalyType = Field(..., description="Type of anomaly")
    severity: AnomalySeverity = Field(..., description="Severity level")
    compte: str = Field(..., description="Compte general concerned")
    section: str = Field(..., description="Section analytique concerned")
    description: str = Field(..., description="Human-readable description")
    current_value: float | None = Field(None, description="Current month value")
    expected_value: float | None = Field(None, description="Expected value based on history")
    z_score: float | None = Field(None, description="Z-score if applicable")
    mean: float | None = Field(None, description="Historical mean")
    std: float | None = Field(None, description="Historical standard deviation")
    historical_values: list[float] = Field(default_factory=list, description="Historical values")


class Pass1Result(BaseModel):
    """Result of Pass 1 (binary pattern detection)."""

    anomalies: list[Anomaly] = Field(default_factory=list)
    nodes_analyzed: int = Field(0)
    disparition_count: int = Field(0)
    apparition_count: int = Field(0)
    variation_count: int = Field(0)
    recurrence_count: int = Field(0)


class Pass2Result(BaseModel):
    """Result of Pass 2 (statistical Z-score analysis)."""

    anomalies: list[Anomaly] = Field(default_factory=list)
    nodes_with_zscore: int = Field(0)
    zscore_anomaly_count: int = Field(0)
    degraded_mode: bool = Field(False, description="True if insufficient baseline data")


class AnalysisResult(BaseModel):
    """Complete analysis result combining Pass 1 and Pass 2."""

    job_id: str
    success: bool
    pass1: Pass1Result
    pass2: Pass2Result
    total_anomalies: int
    confidence_index: float = Field(..., description="Confidence percentage based on data quality")
    processing_time_ms: int
    download_url: str | None = None
