from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict
from app.core.config import settings


class MatchedCondition(BaseModel):
    condition_code: str
    condition_name: str
    confidence_score: float = Field(..., ge=0.0, le=100.0)
    confidence_level: str  # High, Medium, Low
    category: str
    description: Optional[str] = None
    care_recommendations: Optional[str] = None


class SymptomCheckRequest(BaseModel):
    symptoms: List[str] = Field(..., min_length=1, description="List of entered symptoms or keywords")
    age: Optional[int] = Field(None, ge=0, le=130)
    sex: Optional[str] = Field(None, pattern="^(male|female|other)$")
    duration_days: Optional[int] = Field(None, ge=0, le=365)
    severity_scale: Optional[int] = Field(None, ge=1, le=10)
    profile_id: Optional[int] = None


class SymptomCheckResponse(BaseModel):
    session_id: Optional[int] = None
    urgency: str  # emergency, urgent_care, self_care
    red_flags_triggered: List[str] = []
    possible_conditions: List[MatchedCondition] = []
    care_advice: str
    disclaimer: str = settings.MEDICAL_DISCLAIMER


class TriageHistoryItem(BaseModel):
    id: int
    profile_id: Optional[int] = None
    profile_name: Optional[str] = None
    urgency: str
    patient_age: Optional[int] = None
    patient_sex: Optional[str] = None
    duration_days: Optional[int] = None
    severity_scale: Optional[int] = None
    reported_symptoms: List[str]
    possible_conditions: List[MatchedCondition]
    red_flags_triggered: List[str]
    care_advice: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
