"""Pass 3: Excel report generation with multi-tab output.

Generates:
- One tab per anomaly type with detailed findings
- Level 1: Factual statement (what was detected)
- Level 2: Statistical data (Z-score, mean, stddev, history)
- Synthesis tab with aggregated metrics
"""

import tempfile
from pathlib import Path
from datetime import datetime

import xlsxwriter

from api.models.analysis import Anomaly, AnomalyType, AnomalySeverity, Pass1Result, Pass2Result


def create_report(
    pass1_result: Pass1Result,
    pass2_result: Pass2Result,
    confidence_index: float,
    output_path: Path | None = None,
) -> Path:
    """Generate Excel report with analysis results.

    Args:
        pass1_result: Results from Pass 1 (binary detection)
        pass2_result: Results from Pass 2 (Z-score analysis)
        confidence_index: Confidence percentage
        output_path: Optional output path (creates temp file if None)

    Returns:
        Path to the generated Excel file
    """
    if output_path is None:
        tmp = tempfile.NamedTemporaryFile(
            suffix=".xlsx",
            delete=False,
            prefix="controlmyentries_report_"
        )
        output_path = Path(tmp.name)

    workbook = xlsxwriter.Workbook(str(output_path))

    # Define formats
    header_format = workbook.add_format({
        'bold': True,
        'bg_color': '#1e40af',
        'font_color': 'white',
        'border': 1,
        'align': 'center',
        'valign': 'vcenter',
    })

    title_format = workbook.add_format({
        'bold': True,
        'font_size': 14,
        'font_color': '#1e3a8a',
    })

    severity_high = workbook.add_format({
        'bg_color': '#fef2f2',
        'font_color': '#991b1b',
        'border': 1,
    })

    severity_medium = workbook.add_format({
        'bg_color': '#fffbeb',
        'font_color': '#92400e',
        'border': 1,
    })

    severity_low = workbook.add_format({
        'bg_color': '#f0fdf4',
        'font_color': '#166534',
        'border': 1,
    })

    normal_format = workbook.add_format({
        'border': 1,
        'valign': 'vcenter',
    })

    number_format = workbook.add_format({
        'border': 1,
        'num_format': '#,##0.00',
    })

    # Combine all anomalies
    all_anomalies = pass1_result.anomalies + pass2_result.anomalies

    # Create Synthesis tab first
    _create_synthesis_tab(
        workbook,
        all_anomalies,
        pass1_result,
        pass2_result,
        confidence_index,
        header_format,
        title_format,
        normal_format,
        number_format,
    )

    # Create tabs by anomaly type
    anomaly_types = [
        (AnomalyType.DISPARITION, "Disparitions"),
        (AnomalyType.APPARITION, "Apparitions"),
        (AnomalyType.VARIATION, "Variations"),
        (AnomalyType.RECURRENCE, "Recurrences"),
        (AnomalyType.ZSCORE, "Z-Score"),
    ]

    for anomaly_type, tab_name in anomaly_types:
        type_anomalies = [a for a in all_anomalies if a.type == anomaly_type]
        if type_anomalies:
            _create_anomaly_tab(
                workbook,
                tab_name,
                type_anomalies,
                header_format,
                normal_format,
                number_format,
                severity_high,
                severity_medium,
                severity_low,
            )

    workbook.close()
    return output_path


def _create_synthesis_tab(
    workbook,
    all_anomalies: list[Anomaly],
    pass1_result: Pass1Result,
    pass2_result: Pass2Result,
    confidence_index: float,
    header_format,
    title_format,
    normal_format,
    number_format,
):
    """Create the synthesis summary tab."""
    sheet = workbook.add_worksheet("Synthese")
    sheet.set_column('A:A', 30)
    sheet.set_column('B:B', 15)
    sheet.set_column('C:C', 40)

    row = 0

    # Title
    sheet.write(row, 0, "Rapport d'Analyse Controlmyentries", title_format)
    row += 1
    sheet.write(row, 0, f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    row += 2

    # Summary metrics
    sheet.write(row, 0, "Resume de l'Analyse", title_format)
    row += 1

    metrics = [
        ("Noeuds analyses", pass1_result.nodes_analyzed),
        ("Total anomalies detectees", len(all_anomalies)),
        ("Indice de confiance", f"{confidence_index:.1f}%"),
        ("Mode degrade", "Oui" if pass2_result.degraded_mode else "Non"),
    ]

    for metric, value in metrics:
        sheet.write(row, 0, metric, normal_format)
        sheet.write(row, 1, value, normal_format)
        row += 1

    row += 1

    # Breakdown by type
    sheet.write(row, 0, "Repartition par Type", title_format)
    row += 1

    type_counts = [
        ("Disparitions (noeuds absents)", pass1_result.disparition_count),
        ("Apparitions (nouveaux noeuds)", pass1_result.apparition_count),
        ("Variations brutales (>20%)", pass1_result.variation_count),
        ("Recurrences interrompues", pass1_result.recurrence_count),
        ("Anomalies Z-score (|Z|>2)", pass2_result.zscore_anomaly_count),
    ]

    for type_name, count in type_counts:
        sheet.write(row, 0, type_name, normal_format)
        sheet.write(row, 1, count, normal_format)
        row += 1

    row += 1

    # Severity breakdown
    sheet.write(row, 0, "Repartition par Severite", title_format)
    row += 1

    severity_counts = {
        "Haute": len([a for a in all_anomalies if a.severity == AnomalySeverity.HIGH]),
        "Moyenne": len([a for a in all_anomalies if a.severity == AnomalySeverity.MEDIUM]),
        "Basse": len([a for a in all_anomalies if a.severity == AnomalySeverity.LOW]),
    }

    for severity, count in severity_counts.items():
        sheet.write(row, 0, severity, normal_format)
        sheet.write(row, 1, count, normal_format)
        row += 1

    row += 2

    # Disclaimer
    sheet.write(row, 0, "AVERTISSEMENT", title_format)
    row += 1
    sheet.write(row, 0, "Aide a la detection, pas certificat d'absence d'anomalie.")
    row += 1
    sheet.write(row, 0, "Les resultats doivent etre verifies par un expert comptable.")


def _create_anomaly_tab(
    workbook,
    tab_name: str,
    anomalies: list[Anomaly],
    header_format,
    normal_format,
    number_format,
    severity_high,
    severity_medium,
    severity_low,
):
    """Create a tab for a specific anomaly type."""
    sheet = workbook.add_worksheet(tab_name)

    # Set column widths
    sheet.set_column('A:A', 12)  # Severity
    sheet.set_column('B:B', 15)  # Compte
    sheet.set_column('C:C', 15)  # Section
    sheet.set_column('D:D', 50)  # Description
    sheet.set_column('E:E', 15)  # Current Value
    sheet.set_column('F:F', 15)  # Expected Value
    sheet.set_column('G:G', 10)  # Z-Score
    sheet.set_column('H:H', 12)  # Mean
    sheet.set_column('I:I', 12)  # Std Dev

    # Headers
    headers = [
        "Severite",
        "Compte",
        "Section",
        "Constat (Niveau 1)",
        "Valeur Actuelle",
        "Valeur Attendue",
        "Z-Score",
        "Moyenne",
        "Ecart-type",
    ]

    for col, header in enumerate(headers):
        sheet.write(0, col, header, header_format)

    # Data rows
    for row, anomaly in enumerate(anomalies, start=1):
        # Choose format based on severity
        if anomaly.severity == AnomalySeverity.HIGH:
            sev_format = severity_high
        elif anomaly.severity == AnomalySeverity.MEDIUM:
            sev_format = severity_medium
        else:
            sev_format = severity_low

        sheet.write(row, 0, anomaly.severity.value.capitalize(), sev_format)
        sheet.write(row, 1, anomaly.compte, normal_format)
        sheet.write(row, 2, anomaly.section, normal_format)
        sheet.write(row, 3, anomaly.description, normal_format)
        sheet.write(row, 4, anomaly.current_value or 0, number_format)
        sheet.write(row, 5, anomaly.expected_value or 0, number_format)
        sheet.write(row, 6, anomaly.z_score if anomaly.z_score else "-", normal_format)
        sheet.write(row, 7, anomaly.mean or 0, number_format)
        sheet.write(row, 8, anomaly.std or 0, number_format)

    # Auto-filter
    if anomalies:
        sheet.autofilter(0, 0, len(anomalies), len(headers) - 1)
