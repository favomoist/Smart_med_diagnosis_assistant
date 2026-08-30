from datetime import datetime, timezone
import enum
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship as orm_relationship
from sqlalchemy.sql import func
from app.core.database import Base


class RoleEnum(str, enum.Enum):
    PATIENT = "patient"
    CAREGIVER = "caregiver"
    CLINICIAN = "clinician"
    ADMIN = "admin"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=False)
    role = Column(String(50), default=RoleEnum.PATIENT.value, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    profiles = orm_relationship("Profile", back_populates="user", cascade="all, delete-orphan")
    triage_sessions = orm_relationship("TriageSession", back_populates="user", cascade="all, delete-orphan")


class Profile(Base):
    """Profiles allow patients to manage their own baseline data or caregivers to manage dependents."""
    __tablename__ = "profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(255), nullable=False)
    relationship = Column("relationship", String(50), default="self", nullable=False)  # self, child, parent, spouse, dependent
    age = Column(Integer, nullable=True)
    sex = Column(String(20), nullable=True)  # male, female, other
    known_allergies = Column(Text, nullable=True)
    chronic_conditions = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    user = orm_relationship("User", back_populates="profiles")
    triage_sessions = orm_relationship("TriageSession", back_populates="profile")
