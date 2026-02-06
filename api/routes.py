"""API route definitions."""

import tempfile
import uuid
from pathlib import Path

from fastapi import APIRouter, File, HTTPException, UploadFile
from fastapi.responses import JSONResponse

from fastapi.responses import Response

from api.services.validator import validate_file, ValidationResult
from api.services.baseline import generate_baseline_from_gl, baseline_to_json
from api.models.errors import ProblemDetail

router = APIRouter()


@router.get("/health")
async def health_check():
    """Health check endpoint for monitoring."""
    return {"status": "ok"}


@router.post("/analyze")
async def analyze_files(
    files: list[UploadFile] = File(..., description="GL file and optional baseline file")
):
    """Upload GL + optional baseline files for analysis.

    Returns a job_id for tracking progress via WebSocket.
    """
    if not files:
        raise HTTPException(
            status_code=400,
            detail=ProblemDetail(
                type="validation_error",
                title="Aucun fichier fourni",
                status=400,
                detail="Veuillez fournir au moins un fichier GL",
            ).model_dump(),
        )

    if len(files) > 2:
        raise HTTPException(
            status_code=400,
            detail=ProblemDetail(
                type="validation_error",
                title="Trop de fichiers",
                status=400,
                detail="Maximum 2 fichiers autorises (1 GL + 1 baseline)",
            ).model_dump(),
        )

    # Validate each file
    validation_results = []
    for upload_file in files:
        # Save to temp file for validation
        suffix = Path(upload_file.filename or "").suffix
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            content = await upload_file.read()
            tmp.write(content)
            tmp_path = Path(tmp.name)

        try:
            result = validate_file(tmp_path)
            validation_results.append({
                "filename": upload_file.filename,
                "result": result,
            })
        finally:
            # Clean up temp file
            tmp_path.unlink(missing_ok=True)

    # Check for validation errors
    errors = [r for r in validation_results if not r["result"].is_valid]
    if errors:
        error_messages = [
            f"{r['filename']}: {r['result'].message}" for r in errors
        ]
        raise HTTPException(
            status_code=400,
            detail=ProblemDetail(
                type="validation_error",
                title="Fichier(s) invalide(s)",
                status=400,
                detail="; ".join(error_messages),
            ).model_dump(),
        )

    # Check we have at least one GL file
    has_gl = any(r["result"].file_type == "gl" for r in validation_results)
    if not has_gl:
        raise HTTPException(
            status_code=400,
            detail=ProblemDetail(
                type="validation_error",
                title="Fichier GL manquant",
                status=400,
                detail="Veuillez fournir un fichier Grand Livre (Excel ou CSV)",
            ).model_dump(),
        )

    # Generate job ID for progress tracking
    job_id = str(uuid.uuid4())

    return JSONResponse(
        status_code=202,
        content={
            "success": True,
            "job_id": job_id,
            "files_validated": [
                {
                    "filename": r["filename"],
                    "type": r["result"].file_type,
                    "message": r["result"].message,
                }
                for r in validation_results
            ],
            "message": "Fichiers valides. Connectez-vous au WebSocket pour suivre la progression.",
        },
    )


@router.post("/validate")
async def validate_single_file(
    file: UploadFile = File(..., description="File to validate")
):
    """Validate a single file without starting analysis.

    Useful for client-side validation before full submission.
    """
    suffix = Path(file.filename or "").suffix
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        content = await file.read()
        tmp.write(content)
        tmp_path = Path(tmp.name)

    try:
        result = validate_file(tmp_path)
    finally:
        tmp_path.unlink(missing_ok=True)

    if not result.is_valid:
        raise HTTPException(
            status_code=400,
            detail=ProblemDetail(
                type="validation_error",
                title="Fichier invalide",
                status=400,
                detail=result.message,
            ).model_dump(),
        )

    return {
        "success": True,
        "filename": file.filename,
        "type": result.file_type,
        "message": result.message,
        "detected_columns": result.detected_columns[:20],  # Limit columns returned
    }


@router.post("/generate-baseline")
async def generate_baseline(
    file: UploadFile = File(..., description="GL N-1 file with 12 months of data")
):
    """Generate a baseline.json from a GL N-1 file.

    The GL should contain at least 6 months of historical data for statistical analysis.
    Returns a downloadable baseline.json file.
    """
    # Validate file type
    suffix = Path(file.filename or "").suffix.lower()
    if suffix not in ('.xlsx', '.xls', '.csv'):
        raise HTTPException(
            status_code=400,
            detail=ProblemDetail(
                type="validation_error",
                title="Format invalide",
                status=400,
                detail="Le fichier GL doit etre au format Excel (.xlsx, .xls) ou CSV",
            ).model_dump(),
        )

    # Save to temp file
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        content = await file.read()
        tmp.write(content)
        tmp_path = Path(tmp.name)

    try:
        # First validate the file
        validation = validate_file(tmp_path)
        if not validation.is_valid:
            raise HTTPException(
                status_code=400,
                detail=ProblemDetail(
                    type="validation_error",
                    title="Fichier GL invalide",
                    status=400,
                    detail=validation.message,
                ).model_dump(),
            )

        # Generate baseline
        baseline, error = generate_baseline_from_gl(tmp_path)
        if error:
            raise HTTPException(
                status_code=400,
                detail=ProblemDetail(
                    type="generation_error",
                    title="Erreur de generation",
                    status=400,
                    detail=error,
                ).model_dump(),
            )

        # Check minimum data
        if baseline.months_count < 6:
            # Return with warning but still generate
            pass

        # Convert to JSON
        json_content = baseline_to_json(baseline)

        return Response(
            content=json_content,
            media_type="application/json",
            headers={
                "Content-Disposition": 'attachment; filename="baseline.json"',
            },
        )

    finally:
        tmp_path.unlink(missing_ok=True)
