from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict
from app.schemas.triage import TriageHistoryItem


class SharedSummaryCreate(BaseModel):
    session_id: int
    valid_hours: Optional[int] = Field(72, ge=1, le=720, description="Validity period in hours (1 to 30 days)")


class ClinicianNoteCreate(BaseModel):
    notes: str = Field(..., min_length=1, max_length=5000, description="Clinician assessment or consultation notes")


class SharedSummaryResponse(BaseModel):
    token: str
    share_url: str
    expires_at: datetime
    is_expired: bool
    is_revoked: bool
    clinician_notes: Optional[str] = None
    session_details: TriageHistoryItem

    model_config = ConfigDict(from_attributes=True)
