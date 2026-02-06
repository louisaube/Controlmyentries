"""File validation service for GL and baseline files."""

from pathlib import Path
from typing import NamedTuple
import tempfile
import polars as pl

# Required columns for GL files (French and common variations)
REQUIRED_GL_COLUMNS = {
    "compte": ["compte", "compte general", "compte_general", "account", "compte g"],
    "section": ["section", "section analytique", "section_analytique", "analytique", "cost_center"],
    "montant": ["montant", "amount", "debit", "credit", "value"],
    "date": ["date", "date piece", "date_piece", "date comptable", "posting_date"],
}


class ValidationResult(NamedTuple):
    """Result of file validation."""
    is_valid: bool
    file_type: str  # 'gl' or 'baseline'
    message: str
    detected_columns: list[str]
    missing_columns: list[str]


def normalize_column_name(name: str) -> str:
    """Normalize column name for comparison."""
    return name.lower().strip().replace("_", " ").replace("-", " ")


def find_matching_column(columns: list[str], variations: list[str]) -> str | None:
    """Find a column matching any of the variations."""
    normalized_columns = {normalize_column_name(c): c for c in columns}
    for variation in variations:
        normalized = normalize_column_name(variation)
        if normalized in normalized_columns:
            return normalized_columns[normalized]
    return None


def validate_gl_file(file_path: Path) -> ValidationResult:
    """Validate a Grand Livre (GL) Excel or CSV file.

    Args:
        file_path: Path to the file to validate

    Returns:
        ValidationResult with validation status and details
    """
    try:
        # Read file based on extension
        suffix = file_path.suffix.lower()
        if suffix in ('.xlsx', '.xls'):
            df = pl.read_excel(file_path)
        elif suffix == '.csv':
            df = pl.read_csv(file_path)
        else:
            return ValidationResult(
                is_valid=False,
                file_type='gl',
                message=f"Format de fichier non supporte: {suffix}",
                detected_columns=[],
                missing_columns=[],
            )

        columns = df.columns
        missing = []
        matched = {}

        # Check each required column category
        for category, variations in REQUIRED_GL_COLUMNS.items():
            match = find_matching_column(columns, variations)
            if match:
                matched[category] = match
            else:
                missing.append(category)

        if missing:
            missing_names = ", ".join(missing)
            detected_str = ", ".join(columns[:10])  # Show first 10 columns
            return ValidationResult(
                is_valid=False,
                file_type='gl',
                message=f"Colonnes manquantes: {missing_names}. Colonnes detectees: {detected_str}",
                detected_columns=columns,
                missing_columns=missing,
            )

        return ValidationResult(
            is_valid=True,
            file_type='gl',
            message="Fichier GL valide",
            detected_columns=columns,
            missing_columns=[],
        )

    except Exception as e:
        return ValidationResult(
            is_valid=False,
            file_type='gl',
            message=f"Erreur lors de la lecture du fichier: {str(e)}",
            detected_columns=[],
            missing_columns=[],
        )


def validate_baseline_file(file_path: Path) -> ValidationResult:
    """Validate a baseline JSON file.

    Args:
        file_path: Path to the JSON file to validate

    Returns:
        ValidationResult with validation status and details
    """
    import json

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Check required structure
        required_keys = ['version', 'nodes']
        missing = [k for k in required_keys if k not in data]

        if missing:
            return ValidationResult(
                is_valid=False,
                file_type='baseline',
                message=f"Structure baseline invalide. Cles manquantes: {', '.join(missing)}",
                detected_columns=list(data.keys()),
                missing_columns=missing,
            )

        # Check version compatibility
        version = data.get('version', '0.0')
        if not version.startswith('1.'):
            return ValidationResult(
                is_valid=False,
                file_type='baseline',
                message=f"Version baseline non supportee: {version}. Version attendue: 1.x",
                detected_columns=list(data.keys()),
                missing_columns=[],
            )

        # Check nodes is a list
        nodes = data.get('nodes', [])
        if not isinstance(nodes, list):
            return ValidationResult(
                is_valid=False,
                file_type='baseline',
                message="Le champ 'nodes' doit etre une liste",
                detected_columns=list(data.keys()),
                missing_columns=[],
            )

        node_count = len(nodes)
        return ValidationResult(
            is_valid=True,
            file_type='baseline',
            message=f"Baseline valide avec {node_count} noeuds",
            detected_columns=list(data.keys()),
            missing_columns=[],
        )

    except json.JSONDecodeError as e:
        return ValidationResult(
            is_valid=False,
            file_type='baseline',
            message=f"JSON invalide: {str(e)}",
            detected_columns=[],
            missing_columns=[],
        )
    except Exception as e:
        return ValidationResult(
            is_valid=False,
            file_type='baseline',
            message=f"Erreur lors de la lecture: {str(e)}",
            detected_columns=[],
            missing_columns=[],
        )


def validate_file(file_path: Path) -> ValidationResult:
    """Validate a file based on its extension.

    Args:
        file_path: Path to the file to validate

    Returns:
        ValidationResult with validation status and details
    """
    suffix = file_path.suffix.lower()

    if suffix == '.json':
        return validate_baseline_file(file_path)
    elif suffix in ('.xlsx', '.xls', '.csv'):
        return validate_gl_file(file_path)
    else:
        return ValidationResult(
            is_valid=False,
            file_type='unknown',
            message=f"Type de fichier non reconnu: {suffix}",
            detected_columns=[],
            missing_columns=[],
        )
