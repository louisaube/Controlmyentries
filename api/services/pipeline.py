"""Full analysis pipeline orchestrating Pass 1, Pass 2, and Pass 3."""

import json
import tempfile
import time
import uuid
from pathlib import Path

from api.models.baseline import Baseline
from api.models.analysis import AnalysisResult, Pass1Result, Pass2Result
from api.services.validator import validate_file
from api.services.pass1 import run_pass1
from api.services.pass2 import run_pass2, calculate_confidence_index
from api.services.pass3 import create_report
from api.core.websocket import send_step_progress


async def run_analysis_pipeline(
    gl_path: Path,
    baseline_path: Path | None,
    job_id: str,
) -> AnalysisResult:
    """Run the complete analysis pipeline.

    Args:
        gl_path: Path to the GL file
        baseline_path: Optional path to baseline.json
        job_id: Job ID for progress updates

    Returns:
        AnalysisResult with all findings
    """
    start_time = time.time()
    total_anomalies = 0

    # Step 1: Validation (already done before calling pipeline)
    await send_step_progress(job_id, step=1, status="processing")

    # Load baseline if provided
    baseline = None
    if baseline_path and baseline_path.exists():
        try:
            with open(baseline_path, 'r', encoding='utf-8') as f:
                baseline_data = json.load(f)
            baseline = Baseline(**baseline_data)
        except Exception:
            baseline = None

    await send_step_progress(job_id, step=1, status="complete")

    # Step 2: Pass 1 - Binary detection
    await send_step_progress(job_id, step=2, status="processing")

    pass1_result = run_pass1(gl_path, baseline)
    total_anomalies += len(pass1_result.anomalies)

    await send_step_progress(job_id, step=2, anomalies_found=total_anomalies, status="complete")

    # Step 3: Pass 2 - Z-score analysis
    await send_step_progress(job_id, step=3, anomalies_found=total_anomalies, status="processing")

    pass2_result = run_pass2(gl_path, baseline)
    total_anomalies += len(pass2_result.anomalies)

    await send_step_progress(job_id, step=3, anomalies_found=total_anomalies, status="complete")

    # Step 4: Pass 3 - Report generation
    await send_step_progress(job_id, step=4, anomalies_found=total_anomalies, status="processing")

    confidence = calculate_confidence_index(baseline)
    report_path = create_report(pass1_result, pass2_result, confidence)

    await send_step_progress(job_id, step=4, anomalies_found=total_anomalies, status="complete")

    # Step 5: Complete
    processing_time_ms = int((time.time() - start_time) * 1000)
    download_url = f"/api/download/{job_id}"

    await send_step_progress(
        job_id,
        step=5,
        anomalies_found=total_anomalies,
        status="complete",
        download_url=download_url,
    )

    return AnalysisResult(
        job_id=job_id,
        success=True,
        pass1=pass1_result,
        pass2=pass2_result,
        total_anomalies=total_anomalies,
        confidence_index=confidence,
        processing_time_ms=processing_time_ms,
        download_url=download_url,
    )


# Store report paths for download (in production, use Redis or similar)
_report_cache: dict[str, Path] = {}


def store_report(job_id: str, report_path: Path):
    """Store report path for later download."""
    _report_cache[job_id] = report_path


def get_report(job_id: str) -> Path | None:
    """Get report path by job ID."""
    return _report_cache.get(job_id)


def cleanup_report(job_id: str):
    """Clean up report after download."""
    if job_id in _report_cache:
        path = _report_cache.pop(job_id)
        if path.exists():
            path.unlink(missing_ok=True)
