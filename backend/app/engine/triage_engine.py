import re
from typing import List, Dict, Any, Tuple, Optional
from sqlalchemy.orm import Session
from app.models.symptom_condition import Symptom, Condition, SymptomConditionMap, RedFlag
from app.engine.seed_data import SYMPTOMS_DATA, CONDITIONS_DATA, MAPS_DATA, RED_FLAGS_DATA
from app.schemas.triage import MatchedCondition, SymptomCheckResponse
from app.core.config import settings


def normalize_text(text: str) -> str:
    """Normalizes string for robust keyword and symptom matching."""
    text = text.lower().strip()
    # Replace non-alphanumeric characters with space
    text = re.sub(r'[^a-z0-9\s]', ' ', text)
    return " ".join(text.split())


def init_knowledge_base(db: Session) -> None:
    """Seed initial clinical symptoms, conditions, relationships, and red-flags if not present."""
    if db.query(Symptom).first() is not None:
        return  # Already seeded

    # 1. Seed Symptoms
    symptom_objs = {}
    for s in SYMPTOMS_DATA:
        sym = Symptom(
            code=s["code"],
            name=s["name"],
            category=s["category"],
            is_red_flag=s["is_red_flag"],
            guidance=s["guidance"],
            description=s["description"]
        )
        db.add(sym)
        symptom_objs[s["code"]] = sym
    db.commit()

    # 2. Seed Conditions
    condition_objs = {}
    for c in CONDITIONS_DATA:
        cond = Condition(
            code=c["code"],
            name=c["name"],
            category=c["category"],
            typical_urgency=c["typical_urgency"],
            description=c["description"],
            advice=c["advice"],
            care_recommendations=c["care_recommendations"]
        )
        db.add(cond)
        condition_objs[c["code"]] = cond
    db.commit()

    # Refresh objects to get generated IDs
    for code, sym in list(symptom_objs.items()):
        db.refresh(sym)
    for code, cond in list(condition_objs.items()):
        db.refresh(cond)

    # 3. Seed Maps
    for m in MAPS_DATA:
        sym = symptom_objs.get(m["symptom_code"])
        cond = condition_objs.get(m["condition_code"])
        if sym and cond:
            mapping = SymptomConditionMap(
                symptom_id=sym.id,
                condition_id=cond.id,
                weight=m["weight"],
                is_hallmark=m["is_hallmark"]
            )
            db.add(mapping)
    db.commit()

    # 4. Seed Red Flags
    for rf in RED_FLAGS_DATA:
        flag = RedFlag(
            trigger_keyword=rf["trigger_keyword"],
            warning_message=rf["warning_message"],
            emergency_instructions=rf["emergency_instructions"]
        )
        db.add(flag)
    db.commit()


def check_red_flags(raw_symptoms: List[str], db: Session) -> Tuple[bool, List[str]]:
    """Screen for critical emergency red flags with 100% target recall."""
    triggered_warnings = []
    normalized_inputs = [normalize_text(s) for s in raw_symptoms]
    all_text = " ".join(normalized_inputs)

    # Query all active red flags
    red_flags = db.query(RedFlag).all()
    for rf in red_flags:
        kw = normalize_text(rf.trigger_keyword)
        if kw in all_text or any(kw in s or s in kw for s in normalized_inputs if len(s) > 3):
            warning = f"RED FLAG: {rf.warning_message} ({rf.emergency_instructions})"
            if warning not in triggered_warnings:
                triggered_warnings.append(warning)

    # Check for direct red-flag symptoms in database
    for raw in normalized_inputs:
        matched_symptoms = db.query(Symptom).filter(Symptom.is_red_flag == True).all()
        for sym in matched_symptoms:
            sym_name_norm = normalize_text(sym.name)
            sym_code_norm = normalize_text(sym.code.replace('_', ' '))
            if (raw in sym_name_norm or raw in sym_code_norm or
                sym_name_norm in raw or sym_code_norm in raw):
                warning = f"RED FLAG: {sym.name} reported. {sym.guidance or 'Requires urgent evaluation.'}"
                if warning not in triggered_warnings:
                    triggered_warnings.append(warning)

    is_emergency = len(triggered_warnings) > 0
    return is_emergency, triggered_warnings


def match_symptoms_to_entities(raw_symptoms: List[str], db: Session) -> List[Symptom]:
    """Map entered text / codes / natural language keywords to known Symptom entities in DB."""
    matched = []
    matched_ids = set()
    all_symptoms = db.query(Symptom).all()

    for raw in raw_symptoms:
        norm = normalize_text(raw)
        if not norm:
            continue
        words = set(norm.split())

        best_sym = None
        highest_match_score = 0

        for sym in all_symptoms:
            sym_name_norm = normalize_text(sym.name)
            sym_code_norm = normalize_text(sym.code.replace('_', ' '))
            sym_desc_norm = normalize_text(sym.description or "")
            sym_words = set(sym_name_norm.split() + sym_code_norm.split() + sym_desc_norm.split())

            score = 0
            if norm == sym.code or norm == sym_code_norm:
                score = 100
            elif norm == sym_name_norm:
                score = 90
            elif norm in sym_name_norm or sym_name_norm in norm:
                score = 80
            elif norm in sym_code_norm or sym_code_norm in norm:
                score = 75
            else:
                # Word intersection score
                common = words.intersection(sym_words)
                # Ignore common stopwords
                meaningful_common = [w for w in common if w not in {"in", "and", "or", "of", "with", "the", "a", "an", "mild", "severe"}]
                if meaningful_common:
                    score = len(meaningful_common) * 20

            if score > highest_match_score and score >= 20:
                highest_match_score = score
                best_sym = sym

        if best_sym and best_sym.id not in matched_ids:
            matched.append(best_sym)
            matched_ids.add(best_sym.id)

    return matched


def evaluate_triage(
    symptoms: List[str],
    age: Optional[int] = None,
    sex: Optional[str] = None,
    duration_days: Optional[int] = None,
    severity_scale: Optional[int] = None,
    db: Session = None,
) -> SymptomCheckResponse:
    """Core Clinical Triage Engine. Evaluates urgency and computes scored condition matches."""
    if not db:
        raise ValueError("Database session is required for triage evaluation.")

    # 1. Stage 1: Red-Flag Emergency Screener
    is_emergency_flagged, red_flags = check_red_flags(symptoms, db)

    # 2. Stage 2: Symptom Entity Resolution
    matched_symptoms = match_symptoms_to_entities(symptoms, db)
    matched_symptom_ids = [s.id for s in matched_symptoms]

    # 3. Stage 3: Weighted Multi-Condition Scoring
    all_conditions = db.query(Condition).all()
    scored_conditions: List[Dict[str, Any]] = []

    for cond in all_conditions:
        # Get all mapped symptoms for this condition
        maps = db.query(SymptomConditionMap).filter(
            SymptomConditionMap.condition_id == cond.id
        ).all()
        if not maps:
            continue

        total_possible_weight = sum(m.weight + (4.0 if m.is_hallmark else 0.0) for m in maps)
        earned_weight = 0.0
        hallmark_matches = 0

        for m in maps:
            if m.symptom_id in matched_symptom_ids:
                weight = m.weight
                if m.is_hallmark:
                    weight += 4.0
                    hallmark_matches += 1
                earned_weight += weight

        if earned_weight > 0:
            # Baseline percentage match
            raw_score = (earned_weight / total_possible_weight) * 100.0

            # Demographic & Clinical adjustments
            if cond.category == "Cardiovascular" and age and age > 50:
                raw_score = min(100.0, raw_score * 1.15)

            if severity_scale and severity_scale >= 8 and cond.typical_urgency in ["emergency", "urgent_care"]:
                raw_score = min(100.0, raw_score * 1.10)

            if duration_days and duration_days <= 3 and "Acute" in cond.name:
                raw_score = min(100.0, raw_score * 1.05)

            final_score = round(min(100.0, raw_score), 1)

            # Confidence classification
            if final_score >= 70.0 or (hallmark_matches >= 1 and final_score >= 50.0):
                confidence_level = "High"
            elif final_score >= 40.0:
                confidence_level = "Medium"
            else:
                confidence_level = "Low"

            scored_conditions.append({
                "condition_code": cond.code,
                "condition_name": cond.name,
                "confidence_score": final_score,
                "confidence_level": confidence_level,
                "category": cond.category,
                "description": cond.description,
                "care_recommendations": cond.care_recommendations or cond.advice,
                "typical_urgency": cond.typical_urgency,
            })

    # Sort conditions by confidence score descending
    scored_conditions.sort(key=lambda x: x["confidence_score"], reverse=True)
    top_conditions = scored_conditions[:5]

    # 4. Stage 4: Determine Overall Urgency
    if is_emergency_flagged or (severity_scale and severity_scale == 10):
        urgency = "emergency"
    elif top_conditions and top_conditions[0]["typical_urgency"] == "emergency":
        urgency = "emergency"
    elif (
        (top_conditions and top_conditions[0]["typical_urgency"] == "urgent_care")
        or (severity_scale and severity_scale >= 7)
        or (duration_days and duration_days >= 14)
    ):
        urgency = "urgent_care"
    else:
        urgency = "self_care"

    # 5. Stage 5: Formulate Clinical Care Advice
    if urgency == "emergency":
        care_advice = (
            "🚨 CRITICAL ALERT: Your reported symptoms indicate a potential medical emergency. "
            "Please call 911 (or local emergency dispatch) or go to the nearest emergency room immediately. "
            "Do not drive yourself."
        )
    elif urgency == "urgent_care":
        care_advice = (
            "⚠️ URGENT GUIDANCE: Your symptoms warrant prompt in-person clinical evaluation. "
            "Please schedule an appointment with your primary doctor or visit an urgent care clinic within 24 to 48 hours."
        )
    else:
        care_advice = (
            "ℹ️ SELF-CARE GUIDANCE: Your symptoms appear consistent with mild or self-limiting conditions. "
            "Focus on hydration, rest, and supportive remedies. If symptoms worsen, persist beyond a few days, "
            "or new symptoms develop, consult a healthcare provider."
        )

    # Format output models
    matched_models = [
        MatchedCondition(
            condition_code=c["condition_code"],
            condition_name=c["condition_name"],
            confidence_score=c["confidence_score"],
            confidence_level=c["confidence_level"],
            category=c["category"],
            description=c["description"],
            care_recommendations=c["care_recommendations"],
        )
        for c in top_conditions
    ]

    return SymptomCheckResponse(
        urgency=urgency,
        red_flags_triggered=red_flags,
        possible_conditions=matched_models,
        care_advice=care_advice,
        disclaimer=settings.MEDICAL_DISCLAIMER,
    )
