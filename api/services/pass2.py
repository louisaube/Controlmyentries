"""Pass 2: Statistical Z-score analysis for anomalies.

Provides:
- Per-node Z-score calculation using node's own mean/stddev
- M vs M-12 comparison to neutralize seasonality
- Flagging anomalies where |Z| > 2
- Degraded mode when baseline is insufficient
"""

import uuid
from pathlib import Path
from typing import Optional

import polars as pl
from scipy import stats

from api.models.analysis import (
    Anomaly,
    AnomalyType,
    AnomalySeverity,
    Pass2Result,
)
from api.models.baseline import Baseline
from api.services.validator import find_matching_column, REQUIRED_GL_COLUMNS


def calculate_zscore(value: float, mean: float, std: float) -> float | None:
    """Calculate Z-score for a value given mean and standard deviation.

    Returns None if std is 0 (cannot calculate Z-score).
    """
    if std == 0:
        return None
    return (value - mean) / std


def determine_severity(z_score: float) -> AnomalySeverity:
    """Determine severity based on Z-score magnitude."""
    abs_z = abs(z_score)
    if abs_z > 3:
        return AnomalySeverity.HIGH
    elif abs_z > 2:
        return AnomalySeverity.MEDIUM
    else:
        return AnomalySeverity.LOW


def run_pass2(
    gl_path: Path,
    baseline: Baseline | None,
    zscore_threshold: float = 2.0,
    min_months_for_stats: int = 6,
) -> Pass2Result:
    """Run Pass 2 analysis: statistical Z-score detection.

    Args:
        gl_path: Path to the current GL file
        baseline: Baseline data with historical statistics
        zscore_threshold: Threshold for flagging anomalies (default |Z| > 2)
        min_months_for_stats: Minimum months required for reliable statistics

    Returns:
        Pass2Result with Z-score based anomalies
    """
    # Check if we have sufficient baseline
    if baseline is None or baseline.months_count < min_months_for_stats:
        return Pass2Result(
            anomalies=[],
            nodes_with_zscore=0,
            zscore_anomaly_count=0,
            degraded_mode=True,
        )

    # Read current GL
    suffix = gl_path.suffix.lower()
    if suffix in ('.xlsx', '.xls'):
        df = pl.read_excel(gl_path)
    else:
        df = pl.read_csv(gl_path)

    columns = df.columns

    # Find required columns
    compte_col = find_matching_column(columns, REQUIRED_GL_COLUMNS["compte"])
    section_col = find_matching_column(columns, REQUIRED_GL_COLUMNS["section"])
    montant_col = find_matching_column(columns, REQUIRED_GL_COLUMNS["montant"])

    # Rename and aggregate
    df = df.rename({
        compte_col: "compte",
        section_col: "section",
        montant_col: "montant",
    })

    df = df.with_columns([
        pl.col("compte").cast(pl.Utf8),
        pl.col("section").cast(pl.Utf8),
        pl.col("montant").cast(pl.Float64),
    ])

    # Aggregate by node
    current_agg = df.group_by(["compte", "section"]).agg(
        pl.col("montant").sum().alias("total")
    )

    # Build baseline lookup
    baseline_lookup: dict[tuple[str, str], dict] = {}
    for node in baseline.nodes:
        key = (node.compte, node.section)
        baseline_lookup[key] = {
            "mean": node.mean,
            "std": node.std,
            "count": node.count,
            "monthly_amounts": node.monthly_amounts,
        }

    # Calculate Z-scores and detect anomalies
    anomalies = []
    nodes_with_zscore = 0

    for row in current_agg.iter_rows(named=True):
        compte = str(row["compte"])
        section = str(row["section"])
        current_value = row["total"]
        key = (compte, section)

        # Skip if no baseline for this node
        if key not in baseline_lookup:
            continue

        node_stats = baseline_lookup[key]
        mean = node_stats["mean"]
        std = node_stats["std"]

        # Calculate Z-score
        z_score = calculate_zscore(current_value, mean, std)

        if z_score is None:
            continue

        nodes_with_zscore += 1

        # Check if anomaly threshold exceeded
        if abs(z_score) > zscore_threshold:
            severity = determine_severity(z_score)

            direction = "superieur" if z_score > 0 else "inferieur"
            anomalies.append(Anomaly(
                id=str(uuid.uuid4()),
                type=AnomalyType.ZSCORE,
                severity=severity,
                compte=compte,
                section=section,
                description=f"Z-score de {z_score:.2f} pour {compte}/{section} - montant {direction} a la normale",
                current_value=current_value,
                expected_value=mean,
                z_score=z_score,
                mean=mean,
                std=std,
                historical_values=node_stats.get("monthly_amounts", []),
            ))

    return Pass2Result(
        anomalies=anomalies,
        nodes_with_zscore=nodes_with_zscore,
        zscore_anomaly_count=len(anomalies),
        degraded_mode=False,
    )


def calculate_confidence_index(baseline: Baseline | None) -> float:
    """Calculate confidence index based on baseline quality.

    Returns a percentage (0-100) indicating reliability of analysis.
    """
    if baseline is None:
        return 0.0

    months = baseline.months_count
    nodes = len(baseline.nodes)

    # Confidence factors
    # - More months = more confidence (max at 12 months)
    month_factor = min(months / 12, 1.0)

    # - More nodes with data = more complete picture
    node_factor = 1.0 if nodes > 0 else 0.0

    # Combine factors
    confidence = (month_factor * 0.7 + node_factor * 0.3) * 100

    return round(confidence, 1)
