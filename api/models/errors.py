"""Error models following RFC 7807."""

from pydantic import BaseModel


class ProblemDetail(BaseModel):
    """RFC 7807 Problem Details for HTTP APIs."""

    type: str = "about:blank"
    title: str
    status: int
    detail: str
    instance: str | None = None

    class Config:
        json_schema_extra = {
            "example": {
                "type": "validation_error",
                "title": "Colonnes manquantes",
                "status": 400,
                "detail": "Colonnes attendues: Date, Compte, Montant. Detectees: A, B, C",
            }
        }
