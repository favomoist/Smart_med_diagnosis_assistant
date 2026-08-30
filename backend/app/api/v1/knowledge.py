from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.api.deps import require_role
from app.models.symptom_condition import Symptom, Condition, SymptomConditionMap, RedFlag
from app.models.user import User
from app.schemas.knowledge import (
    SymptomCreate,
    SymptomResponse,
    ConditionCreate,
    ConditionResponse,
    SymptomConditionMapCreate,
    RedFlagCreate,
    RedFlagResponse,
)

router = APIRouter()


@router.get("/symptoms", response_model=List[SymptomResponse])
def get_symptoms(
    search: Optional[str] = Query(None, description="Search term for symptom code or name"),
    category: Optional[str] = Query(None, description="Filter by category"),
    db: Session = Depends(get_db)
):
    """Retrieve catalog of clinical symptoms for autocomplete and guided intake."""
    query = db.query(Symptom)
    if search:
        query = query.filter(
            (Symptom.name.ilike(f"%{search}%")) | (Symptom.code.ilike(f"%{search}%"))
        )
    if category:
        query = query.filter(Symptom.category.ilike(f"%{category}%"))
    return query.all()


@router.post("/symptoms", response_model=SymptomResponse, status_code=status.HTTP_201_CREATED)
def create_symptom(
    payload: SymptomCreate,
    current_user: User = Depends(require_role(["admin"])),
    db: Session = Depends(get_db)
):
    """Admin endpoint to create a new symptom entry."""
    existing = db.query(Symptom).filter(Symptom.code == payload.code.lower()).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A symptom with this code already exists."
        )
    sym = Symptom(
        code=payload.code.lower(),
        name=payload.name,
        category=payload.category,
        description=payload.description,
        is_red_flag=payload.is_red_flag,
        guidance=payload.guidance
    )
    db.add(sym)
    db.commit()
    db.refresh(sym)
    return sym


@router.get("/conditions", response_model=List[ConditionResponse])
def get_conditions(
    search: Optional[str] = Query(None, description="Search term for condition code or name"),
    category: Optional[str] = Query(None, description="Filter by category"),
    db: Session = Depends(get_db)
):
    """Retrieve list of medical conditions."""
    query = db.query(Condition)
    if search:
        query = query.filter(
            (Condition.name.ilike(f"%{search}%")) | (Condition.code.ilike(f"%{search}%"))
        )
    if category:
        query = query.filter(Condition.category.ilike(f"%{category}%"))
    return query.all()


@router.post("/conditions", response_model=ConditionResponse, status_code=status.HTTP_201_CREATED)
def create_condition(
    payload: ConditionCreate,
    current_user: User = Depends(require_role(["admin"])),
    db: Session = Depends(get_db)
):
    """Admin endpoint to create a new condition."""
    existing = db.query(Condition).filter(Condition.code == payload.code.lower()).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A condition with this code already exists."
        )
    cond = Condition(
        code=payload.code.lower(),
        name=payload.name,
        category=payload.category,
        typical_urgency=payload.typical_urgency,
        description=payload.description,
        advice=payload.advice,
        care_recommendations=payload.care_recommendations
    )
    db.add(cond)
    db.commit()
    db.refresh(cond)
    return cond


@router.post("/map", status_code=status.HTTP_201_CREATED)
def create_symptom_condition_map(
    payload: SymptomConditionMapCreate,
    current_user: User = Depends(require_role(["admin"])),
    db: Session = Depends(get_db)
):
    """Admin endpoint to create a weighted clinical link between a symptom and a condition."""
    sym = db.query(Symptom).filter(Symptom.code == payload.symptom_code.lower()).first()
    if not sym:
        raise HTTPException(status_code=404, detail="Symptom not found")
    cond = db.query(Condition).filter(Condition.code == payload.condition_code.lower()).first()
    if not cond:
        raise HTTPException(status_code=404, detail="Condition not found")

    existing_map = db.query(SymptomConditionMap).filter(
        SymptomConditionMap.symptom_id == sym.id,
        SymptomConditionMap.condition_id == cond.id
    ).first()

    if existing_map:
        existing_map.weight = payload.weight
        existing_map.is_hallmark = payload.is_hallmark
    else:
        mapping = SymptomConditionMap(
            symptom_id=sym.id,
            condition_id=cond.id,
            weight=payload.weight,
            is_hallmark=payload.is_hallmark
        )
        db.add(mapping)

    db.commit()
    return {"status": "success", "message": "Mapping recorded successfully"}


@router.get("/red-flags", response_model=List[RedFlagResponse])
def get_red_flags(db: Session = Depends(get_db)):
    """List all registered critical red-flag triggers."""
    return db.query(RedFlag).all()


@router.post("/red-flags", response_model=RedFlagResponse, status_code=status.HTTP_201_CREATED)
def create_red_flag(
    payload: RedFlagCreate,
    current_user: User = Depends(require_role(["admin"])),
    db: Session = Depends(get_db)
):
    """Admin endpoint to register a new clinical red-flag trigger."""
    flag = RedFlag(
        trigger_keyword=payload.trigger_keyword.lower(),
        warning_message=payload.warning_message,
        emergency_instructions=payload.emergency_instructions
    )
    db.add(flag)
    db.commit()
    db.refresh(flag)
    return flag
