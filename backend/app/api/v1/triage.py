import json
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.api.deps import get_current_user_optional, get_current_user
from app.models.user import User, Profile
from app.models.triage import TriageSession
from app.engine.triage_engine import evaluate_triage
from app.schemas.triage import (
    SymptomCheckRequest,
    SymptomCheckResponse,
    TriageHistoryItem,
    MatchedCondition,
)

router = APIRouter()


@router.post("/check", response_model=SymptomCheckResponse)
def perform_symptom_check(
    payload: SymptomCheckRequest,
    current_user: Optional[User] = Depends(get_current_user_optional),
    db: Session = Depends(get_db)
):
    """
    Core Symptom Intake and Clinical Triage API.
    Evaluates urgency level, detects emergency red flags, computes condition likelihood scores,
    and returns actionable medical care guidance.
    """
    age = payload.age
    sex = payload.sex
    profile_id = payload.profile_id

    # If profile_id is provided and user is authenticated, retrieve profile baseline
    profile_name = None
    if current_user and profile_id:
        profile = db.query(Profile).filter(
            Profile.id == profile_id,
            Profile.user_id == current_user.id
        ).first()
        if profile:
            age = age or profile.age
            sex = sex or profile.sex
            profile_name = profile.name

    # Execute Clinical Triage Engine
    triage_result = evaluate_triage(
        symptoms=payload.symptoms,
        age=age,
        sex=sex,
        duration_days=payload.duration_days,
        severity_scale=payload.severity_scale,
        db=db,
    )

    # Persist session if user is logged in
    session_id = None
    if current_user:
        new_session = TriageSession(
            user_id=current_user.id,
            profile_id=profile_id,
            urgency=triage_result.urgency,
            patient_age=age,
            patient_sex=sex,
            duration_days=payload.duration_days,
            severity_scale=payload.severity_scale,
            reported_symptoms_json=json.dumps(payload.symptoms),
            matched_conditions_json=json.dumps([c.model_dump() for c in triage_result.possible_conditions]),
            red_flags_triggered_json=json.dumps(triage_result.red_flags_triggered),
            care_advice=triage_result.care_advice,
        )
        db.add(new_session)
        db.commit()
        db.refresh(new_session)
        session_id = new_session.id

    triage_result.session_id = session_id
    return triage_result


@router.get("/history", response_model=List[TriageHistoryItem])
def get_triage_history(
    profile_id: Optional[int] = Query(None, description="Filter history by profile ID"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Retrieve chronological symptom check and triage history for the authenticated user."""
    query = db.query(TriageSession).filter(TriageSession.user_id == current_user.id)
    if profile_id:
        query = query.filter(TriageSession.profile_id == profile_id)
    
    sessions = query.order_by(TriageSession.created_at.desc()).all()

    history = []
    for s in sessions:
        conditions_data = json.loads(s.matched_conditions_json) if s.matched_conditions_json else []
        matched_conditions = [MatchedCondition(**c) for c in conditions_data]
        symptoms_list = json.loads(s.reported_symptoms_json) if s.reported_symptoms_json else []
        red_flags_list = json.loads(s.red_flags_triggered_json) if s.red_flags_triggered_json else []
        profile_name = s.profile.name if s.profile else None

        history.append(
            TriageHistoryItem(
                id=s.id,
                profile_id=s.profile_id,
                profile_name=profile_name,
                urgency=s.urgency,
                patient_age=s.patient_age,
                patient_sex=s.patient_sex,
                duration_days=s.duration_days,
                severity_scale=s.severity_scale,
                reported_symptoms=symptoms_list,
                possible_conditions=matched_conditions,
                red_flags_triggered=red_flags_list,
                care_advice=s.care_advice,
                created_at=s.created_at,
            )
        )
    return history


@router.get("/sessions/{session_id}", response_model=TriageHistoryItem)
def get_triage_session(
    session_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get full details of a specific past triage session."""
    session = db.query(TriageSession).filter(
        TriageSession.id == session_id,
        TriageSession.user_id == current_user.id
    ).first()

    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Triage session not found"
        )

    conditions_data = json.loads(session.matched_conditions_json) if session.matched_conditions_json else []
    matched_conditions = [MatchedCondition(**c) for c in conditions_data]
    symptoms_list = json.loads(session.reported_symptoms_json) if session.reported_symptoms_json else []
    red_flags_list = json.loads(session.red_flags_triggered_json) if session.red_flags_triggered_json else []

    return TriageHistoryItem(
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
