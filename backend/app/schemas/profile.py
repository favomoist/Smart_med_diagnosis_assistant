from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict


class ProfileCreate(BaseModel):
    name: str
    relationship: Optional[str] = "self"  # self, child, parent, spouse, dependent
    age: Optional[int] = None
    sex: Optional[str] = None  # male, female, other
    known_allergies: Optional[str] = None
    chronic_conditions: Optional[str] = None


class ProfileUpdate(BaseModel):
    name: Optional[str] = None
    relationship: Optional[str] = None
    age: Optional[int] = None
    sex: Optional[str] = None
    known_allergies: Optional[str] = None
    chronic_conditions: Optional[str] = None


class ProfileResponse(BaseModel):
    id: int
    user_id: int
    name: str
    relationship: str
    age: Optional[int] = None
    sex: Optional[str] = None
    known_allergies: Optional[str] = None
    chronic_conditions: Optional[str] = None
    created_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
