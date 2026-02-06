"""Baseline generation service."""

import json
from datetime import date
from pathlib import Path
from statistics import mean, stdev

import polars as pl

from api.models.baseline import Baseline, NodeStatistics
from api.services.validator import find_matching_column, REQUIRED_GL_COLUMNS


def generate_baseline_from_gl(file_path: Path) -> tuple[Baseline, str]:
    """Generate a baseline from a GL file containing historical data.

    Args:
        file_path: Path to the GL file (Excel or CSV)

    Returns:
        Tuple of (Baseline object, error message if any)
    """
    try:
        # Read file
        suffix = file_path.suffix.lower()
        if suffix in ('.xlsx', '.xls'):
            df = pl.read_excel(file_path)
        elif suffix == '.csv':
            df = pl.read_csv(file_path)
        else:
            return None, f"Format non supporte: {suffix}"

        columns = df.columns

        # Find required columns
        compte_col = find_matching_column(columns, REQUIRED_GL_COLUMNS["compte"])
        section_col = find_matching_column(columns, REQUIRED_GL_COLUMNS["section"])
        montant_col = find_matching_column(columns, REQUIRED_GL_COLUMNS["montant"])
        date_col = find_matching_column(columns, REQUIRED_GL_COLUMNS["date"])

        if not all([compte_col, section_col, montant_col, date_col]):
            missing = []
            if not compte_col:
                missing.append("compte")
            if not section_col:
                missing.append("section")
            if not montant_col:
                missing.append("montant")
            if not date_col:
                missing.append("date")
            return None, f"Colonnes manquantes: {', '.join(missing)}"

        # Rename columns for consistency
        df = df.rename({
            compte_col: "compte",
            section_col: "section",
            montant_col: "montant",
            date_col: "date",
        })

        # Parse dates and extract year-month
        df = df.with_columns([
            pl.col("date").cast(pl.Utf8).alias("date_str"),
            pl.col("compte").cast(pl.Utf8),
            pl.col("section").cast(pl.Utf8),
            pl.col("montant").cast(pl.Float64),
        ])

        # Try to parse date to get period
        try:
            df = df.with_columns(
                pl.col("date").str.slice(0, 7).alias("period")  # YYYY-MM format
            )
        except Exception:
            # Fallback: use date as-is
            df = df.with_columns(
                pl.col("date_str").str.slice(0, 7).alias("period")
            )

        # Get period range
        periods = df["period"].unique().sort().to_list()
        period_start = periods[0] if periods else None
        period_end = periods[-1] if periods else None
        months_count = len(periods)

        # Group by node (compte x section) and aggregate
        node_stats = []

        grouped = df.group_by(["compte", "section", "period"]).agg(
            pl.col("montant").sum().alias("total")
        )

        # Pivot to get monthly amounts per node
        nodes = grouped.group_by(["compte", "section"]).agg([
            pl.col("total").alias("monthly_amounts"),
        ])

        for row in nodes.iter_rows(named=True):
            amounts = row["monthly_amounts"]
            if not amounts:
                continue

            # Calculate statistics
            node_mean = mean(amounts) if amounts else 0.0
            node_std = stdev(amounts) if len(amounts) > 1 else 0.0

            node_stats.append(NodeStatistics(
                compte=str(row["compte"]),
                section=str(row["section"]),
                monthly_amounts=amounts,
                mean=round(node_mean, 2),
                std=round(node_std, 2),
                count=len(amounts),
                min_amount=min(amounts),
                max_amount=max(amounts),
            ))

        baseline = Baseline(
            version="1.0",
            generated=date.today().isoformat(),
            project="Controlmyentries",
            period_start=period_start,
            period_end=period_end,
            months_count=months_count,
            nodes=node_stats,
        )

        return baseline, ""

    except Exception as e:
        return None, f"Erreur lors de la generation: {str(e)}"


def baseline_to_json(baseline: Baseline) -> str:
    """Convert baseline to JSON string."""
    return baseline.model_dump_json(indent=2)
