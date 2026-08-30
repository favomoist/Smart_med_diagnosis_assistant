from typing import Optional
from pydantic import BaseModel, ConfigDict


class SymptomBase(BaseModel):
    code: str
    name: str
    category: str = "General"
    description: Optional[str] = None
    is_red_flag: bool = False
    guidance: Optional[str] = None


class SymptomCreate(SymptomBase):
    pass


class SymptomResponse(SymptomBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class ConditionBase(BaseModel):
    code: str
    name: str
    category: str = "General"
    description: Optional[str] = None
    typical_urgency: str = "self_care"  # emergency, urgent_care, self_care
    advice: Optional[str] = None
    care_recommendations: Optional[str] = None


class ConditionCreate(ConditionBase):
    pass


class ConditionResponse(ConditionBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class SymptomConditionMapCreate(BaseModel):
    symptom_code: str
    condition_code: str
    weight: float = 1.0
    is_hallmark: bool = False


class RedFlagCreate(BaseModel):
    trigger_keyword: str
    warning_message: str
    emergency_instructions: str


class RedFlagResponse(RedFlagCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)
