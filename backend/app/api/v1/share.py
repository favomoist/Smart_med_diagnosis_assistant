import secrets
import json
from datetime import datetime, timezone, timedelta
from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.api.deps import get_current_user, get_current_user_optional, require_role
from app.models.user import User
from app.models.triage import TriageSession, SharedSummary
from app.schemas.share import (
    SharedSummaryCreate,
    SharedSummaryResponse,
    ClinicianNoteCreate,
)
from app.schemas.triage import TriageHistoryItem, MatchedCondition

router = APIRouter()


@router.post("/create", response_model=SharedSummaryResponse, status_code=status.HTTP_201_CREATED)
def create_shareable_summary(
    payload: SharedSummaryCreate,
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Generate a secure cryptographic token for sharing a triage summary with a clinician."""
    session = db.query(TriageSession).filter(
        TriageSession.id == payload.session_id,
        TriageSession.user_id == current_user.id
    ).first()

    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Triage session not found"
        )

    # Generate crypto-random token
    share_token = secrets.token_urlsafe(32)
    valid_hours = payload.valid_hours or 72
    expires_at = datetime.now(timezone.utc) + timedelta(hours=valid_hours)

    shared_summary = SharedSummary(
        session_id=session.id,
        token=share_token,
        created_by_user_id=current_user.id,
        expires_at=expires_at,
        is_revoked=False
    )
    db.add(shared_summary)
    db.commit()
    db.refresh(shared_summary)

    base_url = str(request.base_url).rstrip("/")
    share_url = f"{base_url}/api/v1/share/{share_token}"

    conditions_data = json.loads(session.matched_conditions_json) if session.matched_conditions_json else []
    matched_conditions = [MatchedCondition(**c) for c in conditions_data]
    symptoms_list = json.loads(session.reported_symptoms_json) if session.reported_symptoms_json else []
    red_flags_list = json.loads(session.red_flags_triggered_json) if session.red_flags_triggered_json else []

    session_details = TriageHistoryItem(
        id=session.id,
        profile_id=session.profile_id,
        profile_name=session.profile.name if session.profile else None,
        urgency=session.urgency,
        patient_age=session.patient_age,
        patient_sex=session.patient_sex,
        duration_days=session.duration_days,
        severity_scale=session.severity_scale,
        reported_symptoms=symptoms_list,
        possible_conditions=matched_conditions,
        red_flags_triggered=red_flags_list,
        care_advice=session.care_advice,
        created_at=session.created_at,
    )

    return SharedSummaryResponse(
        token=share_token,
        share_url=share_url,
        expires_at=expires_at,
        is_expired=False,
        is_revoked=False,
        clinician_notes=None,
        session_details=session_details,
    )


@router.get("/{token}", response_model=SharedSummaryResponse)
def get_shared_summary(
    token: str,
    request: Request,
    db: Session = Depends(get_db)
):
    """View structured pre-consultation patient summary via sharing token."""
    summary = db.query(SharedSummary).filter(SharedSummary.token == token).first()
    if not summary:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Shared summary not found or invalid token."
        )

    # Check expiration and revocation
    # Handle timezone comparison
    expires = summary.expires_at
    if expires.tzinfo is None:
        expires = expires.replace(tzinfo=timezone.utc)
    is_expired = datetime.now(timezone.utc) > expires

    if summary.is_revoked or is_expired:
        raise HTTPException(
            status_code=status.HTTP_410_GONE,
            detail="This shared summary link has expired or been revoked."
        )

    session = summary.session
    conditions_data = json.loads(session.matched_conditions_json) if session.matched_conditions_json else []
    matched_conditions = [MatchedCondition(**c) for c in conditions_data]
    symptoms_list = json.loads(session.reported_symptoms_json) if session.reported_symptoms_json else []
    red_flags_list = json.loads(session.red_flags_triggered_json) if session.red_flags_triggered_json else []

    base_url = str(request.base_url).rstrip("/")
    share_url = f"{base_url}/api/v1/share/{token}"

    session_details = TriageHistoryItem(
        id=session.id,
        profile_id=session.profile_id,
        profile_name=session.profile.name if session.profile else None,
        urgency=session.urgency,
        patient_age=session.patient_age,
        patient_sex=session.patient_sex,
        duration_days=session.duration_days,
        severity_scale=session.severity_scale,
        reported_symptoms=symptoms_list,
        possible_conditions=matched_conditions,
        red_flags_triggered=red_flags_list,
        care_advice=session.care_advice,
        created_at=session.created_at,
    )

    return SharedSummaryResponse(
        token=token,
        share_url=share_url,
        expires_at=summary.expires_at,
        is_expired=is_expired,
        is_revoked=summary.is_revoked,
        clinician_notes=summary.clinician_notes,
        session_details=session_details,
    )


@router.post("/{token}/notes", response_model=SharedSummaryResponse)
def add_clinician_note(
    token: str,
    payload: ClinicianNoteCreate,
    request: Request,
    current_user: User = Depends(require_role(["clinician", "admin"])),
    db: Session = Depends(get_db)
):
    """Allows a licensed clinician to add assessment/consultation notes to the shared summary."""
    summary = db.query(SharedSummary).filter(SharedSummary.token == token).first()
    if not summary:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Shared summary not found"
        )

    summary.clinician_notes = payload.notes
    summary.clinician_id = current_user.id
    db.commit()
    db.refresh(summary)

    session = summary.session
    conditions_data = json.loads(session.matched_conditions_json) if session.matched_conditions_json else []
    matched_conditions = [MatchedCondition(**c) for c in conditions_data]
    symptoms_list = json.loads(session.reported_symptoms_json) if session.reported_symptoms_json else []
    red_flags_list = json.loads(session.red_flags_triggered_json) if session.red_flags_triggered_json else []

    base_url = str(request.base_url).rstrip("/")
    share_url = f"{base_url}/api/v1/share/{token}"

    session_details = TriageHistoryItem(
        id=session.id,
        profile_id=session.profile_id,
        profile_name=session.profile.name if session.profile else None,
        urgency=session.urgency,
        patient_age=session.patient_age,
        patient_sex=session.patient_sex,
        duration_days=session.duration_days,
        severity_scale=session.severity_scale,
        reported_symptoms=symptoms_list,
        possible_conditions=matched_conditions,
        red_flags_triggered=red_flags_list,
        care_advice=session.care_advice,
        created_at=session.created_at,
    )

    return SharedSummaryResponse(
        token=token,
        share_url=share_url,
        expires_at=summary.expires_at,
        is_expired=False,
        is_revoked=summary.is_revoked,
        clinician_notes=summary.clinician_notes,
        session_details=session_details,
    )
