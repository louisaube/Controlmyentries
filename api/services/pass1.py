"""Pass 1: Binary pattern detection for anomalies.

Detects:
- Disparition: Node was active in previous months, absent in current month
- Apparition: New node appeared (not in history)
- Variation: Brutal variation > 20% from trend
- Recurrence: Broken recurrence pattern (regular entries stopped)
"""

import uuid
from pathlib import Path

import polars as pl

from api.models.analysis import (
    Anomaly,
    AnomalyType,
    AnomalySeverity,
    Pass1Result,
)
from api.models.baseline import Baseline
from api.services.validator import find_matching_column, REQUIRED_GL_COLUMNS


def detect_disparition(
    baseline_nodes: dict[tuple[str, str], dict],
    current_nodes: set[tuple[str, str]],
) -> list[Anomaly]:
    """Detect nodes that disappeared (were active, now absent)."""
    anomalies = []

    for node_key, stats in baseline_nodes.items():
        if node_key not in current_nodes:
            compte, section = node_key
            # Node was active but is now absent
            anomalies.append(Anomaly(
                id=str(uuid.uuid4()),
                type=AnomalyType.DISPARITION,
                severity=AnomalySeverity.MEDIUM,
                compte=compte,
                section=section,
                description=f"Le noeud {compte}/{section} etait actif les mois precedents mais est absent ce mois-ci",
                current_value=0,
                expected_value=stats.get("mean", 0),
                mean=stats.get("mean"),
                std=stats.get("std"),
                historical_values=stats.get("monthly_amounts", []),
            ))

    return anomalies


def detect_apparition(
    baseline_nodes: dict[tuple[str, str], dict],
    current_data: dict[tuple[str, str], float],
    threshold: float = 100,  # Minimum amount to flag as significant
) -> list[Anomaly]:
    """Detect new nodes that appeared (not in historical baseline)."""
    anomalies = []

    for node_key, amount in current_data.items():
        if node_key not in baseline_nodes and abs(amount) >= threshold:
            compte, section = node_key
            anomalies.append(Anomaly(
                id=str(uuid.uuid4()),
                type=AnomalyType.APPARITION,
                severity=AnomalySeverity.MEDIUM,
                compte=compte,
                section=section,
                description=f"Nouveau noeud {compte}/{section} apparu ce mois avec un montant de {amount:.2f}",
                current_value=amount,
                expected_value=0,
            ))

    return anomalies


def detect_variation(
    baseline_nodes: dict[tuple[str, str], dict],
    current_data: dict[tuple[str, str], float],
    threshold_pct: float = 0.20,  # 20% variation threshold
) -> list[Anomaly]:
    """Detect brutal variations > threshold from historical mean."""
    anomalies = []

    for node_key, current_value in current_data.items():
        if node_key not in baseline_nodes:
            continue

        stats = baseline_nodes[node_key]
        mean_value = stats.get("mean", 0)

        if mean_value == 0:
            continue

        variation_pct = abs(current_value - mean_value) / abs(mean_value)

        if variation_pct > threshold_pct:
            compte, section = node_key
            severity = AnomalySeverity.HIGH if variation_pct > 0.5 else AnomalySeverity.MEDIUM

            anomalies.append(Anomaly(
                id=str(uuid.uuid4()),
                type=AnomalyType.VARIATION,
                severity=severity,
                compte=compte,
                section=section,
                description=f"Variation de {variation_pct*100:.1f}% pour {compte}/{section} (attendu: {mean_value:.2f}, observe: {current_value:.2f})",
                current_value=current_value,
                expected_value=mean_value,
                mean=mean_value,
                std=stats.get("std"),
                historical_values=stats.get("monthly_amounts", []),
            ))

    return anomalies


def detect_recurrence(
    baseline_nodes: dict[tuple[str, str], dict],
    current_data: dict[tuple[str, str], float],
    min_occurrences: int = 6,  # Minimum months to establish recurrence
) -> list[Anomaly]:
    """Detect broken recurrence patterns (regular entries that stopped)."""
    anomalies = []

    for node_key, stats in baseline_nodes.items():
        monthly_amounts = stats.get("monthly_amounts", [])
        count = stats.get("count", 0)

        # Need enough history to establish a pattern
        if count < min_occurrences:
            continue

        # Check if all historical values are non-zero (regular pattern)
        non_zero_ratio = sum(1 for v in monthly_amounts if v != 0) / len(monthly_amounts)

        if non_zero_ratio >= 0.8:  # 80% of months had entries
            current_value = current_data.get(node_key, 0)
            if current_value == 0:  # Pattern broken - no entry this month
                compte, section = node_key
                anomalies.append(Anomaly(
                    id=str(uuid.uuid4()),
                    type=AnomalyType.RECURRENCE,
                    severity=AnomalySeverity.MEDIUM,
                    compte=compte,
                    section=section,
                    description=f"Interruption de recurrence pour {compte}/{section} - ce noeud avait des ecritures regulieres",
                    current_value=0,
                    expected_value=stats.get("mean", 0),
                    mean=stats.get("mean"),
                    std=stats.get("std"),
                    historical_values=monthly_amounts,
                ))

    return anomalies


def run_pass1(
    gl_path: Path,
    baseline: Baseline | None,
) -> Pass1Result:
    """Run Pass 1 analysis: binary pattern detection.

    Args:
        gl_path: Path to the current GL file
        baseline: Baseline data (optional, some detectors require it)

    Returns:
        Pass1Result with detected anomalies
    """
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

    # Build current data dict
    current_data: dict[tuple[str, str], float] = {}
    current_nodes: set[tuple[str, str]] = set()

    for row in current_agg.iter_rows(named=True):
        key = (str(row["compte"]), str(row["section"]))
        current_data[key] = row["total"]
        current_nodes.add(key)

    # Build baseline nodes dict
    baseline_nodes: dict[tuple[str, str], dict] = {}
    if baseline:
        for node in baseline.nodes:
            key = (node.compte, node.section)
            baseline_nodes[key] = {
                "mean": node.mean,
                "std": node.std,
                "count": node.count,
                "monthly_amounts": node.monthly_amounts,
            }

    # Run detectors
    all_anomalies = []

    if baseline:
        disparition = detect_disparition(baseline_nodes, current_nodes)
        all_anomalies.extend(disparition)

        apparition = detect_apparition(baseline_nodes, current_data)
        all_anomalies.extend(apparition)

        variation = detect_variation(baseline_nodes, current_data)
        all_anomalies.extend(variation)

        recurrence = detect_recurrence(baseline_nodes, current_data)
        all_anomalies.extend(recurrence)
    else:
        # Without baseline, only apparition detection works (all nodes are "new")
        disparition = []
        apparition = []
        variation = []
        recurrence = []

    return Pass1Result(
        anomalies=all_anomalies,
        nodes_analyzed=len(current_nodes),
        disparition_count=len([a for a in all_anomalies if a.type == AnomalyType.DISPARITION]),
        apparition_count=len([a for a in all_anomalies if a.type == AnomalyType.APPARITION]),
        variation_count=len([a for a in all_anomalies if a.type == AnomalyType.VARIATION]),
        recurrence_count=len([a for a in all_anomalies if a.type == AnomalyType.RECURRENCE]),
    )
