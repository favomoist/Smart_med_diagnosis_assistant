from sqlalchemy import Column, Integer, String, Boolean, Text, ForeignKey, Float
from sqlalchemy.orm import relationship
from app.core.database import Base


class Symptom(Base):
    __tablename__ = "symptoms"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(100), unique=True, index=True, nullable=False)
    name = Column(String(255), nullable=False, index=True)
    category = Column(String(100), nullable=False, default="General")
    description = Column(Text, nullable=True)
    is_red_flag = Column(Boolean, default=False, nullable=False)
    guidance = Column(Text, nullable=True)

    # Relationships
    condition_maps = relationship("SymptomConditionMap", back_populates="symptom", cascade="all, delete-orphan")


class Condition(Base):
    __tablename__ = "conditions"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(100), unique=True, index=True, nullable=False)
    name = Column(String(255), nullable=False, index=True)
    category = Column(String(100), nullable=False, default="General")
    description = Column(Text, nullable=True)
    typical_urgency = Column(String(50), nullable=False, default="self_care")  # emergency, urgent_care, self_care
    advice = Column(Text, nullable=True)
    care_recommendations = Column(Text, nullable=True)

    # Relationships
    symptom_maps = relationship("SymptomConditionMap", back_populates="condition", cascade="all, delete-orphan")


class SymptomConditionMap(Base):
    __tablename__ = "symptom_condition_maps"

    id = Column(Integer, primary_key=True, index=True)
    symptom_id = Column(Integer, ForeignKey("symptoms.id", ondelete="CASCADE"), nullable=False)
    condition_id = Column(Integer, ForeignKey("conditions.id", ondelete="CASCADE"), nullable=False)
    weight = Column(Float, default=1.0, nullable=False)  # 1.0 to 10.0 clinical correlation weight
    is_hallmark = Column(Boolean, default=False, nullable=False)

    # Relationships
    symptom = relationship("Symptom", back_populates="condition_maps")
    condition = relationship("Condition", back_populates="symptom_maps")


class RedFlag(Base):
    __tablename__ = "red_flags"

    id = Column(Integer, primary_key=True, index=True)
    trigger_keyword = Column(String(255), unique=True, index=True, nullable=False)
    warning_message = Column(Text, nullable=False)
    emergency_instructions = Column(Text, nullable=False)
