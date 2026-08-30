from sqlalchemy import Column, Integer, String, Boolean, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class TriageSession(Base):
    __tablename__ = "triage_sessions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    profile_id = Column(Integer, ForeignKey("profiles.id", ondelete="SET NULL"), nullable=True)
    
    urgency = Column(String(50), nullable=False)  # emergency, urgent_care, self_care
    patient_age = Column(Integer, nullable=True)
    patient_sex = Column(String(20), nullable=True)
    duration_days = Column(Integer, nullable=True)
    severity_scale = Column(Integer, nullable=True)  # 1 to 10
    
    reported_symptoms_json = Column(Text, nullable=False)  # Stored as JSON list of strings
    matched_conditions_json = Column(Text, nullable=False)  # Stored as JSON list of scored condition objects
    red_flags_triggered_json = Column(Text, nullable=False)  # Stored as JSON list of triggered red-flag texts
    
    care_advice = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    user = relationship("User", back_populates="triage_sessions")
    profile = relationship("Profile", back_populates="triage_sessions")
    shared_summaries = relationship("SharedSummary", back_populates="session", cascade="all, delete-orphan")


class SharedSummary(Base):
    """Secure shareable pre-consultation summary with clinicians."""
    __tablename__ = "shared_summaries"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("triage_sessions.id", ondelete="CASCADE"), nullable=False)
    token = Column(String(64), unique=True, index=True, nullable=False)
    created_by_user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=True)
    expires_at = Column(DateTime(timezone=True), nullable=False)
    is_revoked = Column(Boolean, default=False, nullable=False)
    
    clinician_notes = Column(Text, nullable=True)
    clinician_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    session = relationship("TriageSession", back_populates="shared_summaries")
