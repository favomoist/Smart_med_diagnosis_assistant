def test_red_flag_chest_pain_emergency(client):
    """Test 100% recall requirement for red-flag cardiovascular emergency."""
    payload = {
        "symptoms": ["chest pain", "shortness of breath", "sweating"],
        "age": 55,
        "sex": "male",
        "duration_days": 1,
        "severity_scale": 9
    }
    response = client.post("/api/v1/triage/check", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["urgency"] == "emergency"
    assert len(data["red_flags_triggered"]) >= 1
    assert any("chest pain" in rf.lower() or "cardiovascular" in rf.lower() for rf in data["red_flags_triggered"])
    assert "911" in data["care_advice"] or "emergency" in data["care_advice"].lower()
    assert "NOT a substitute" in data["disclaimer"]


def test_red_flag_stroke_emergency(client):
    """Test emergency classification for sudden neurological deficits."""
    payload = {
        "symptoms": ["slurred speech", "facial droop", "arm weakness"],
        "age": 62,
        "sex": "female",
        "duration_days": 1,
        "severity_scale": 8
    }
    response = client.post("/api/v1/triage/check", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["urgency"] == "emergency"
    assert len(data["red_flags_triggered"]) >= 1
    # Check top condition matches stroke
    top_cond = data["possible_conditions"][0]
    assert "Stroke" in top_cond["condition_name"]
    assert top_cond["confidence_level"] in ["High", "Medium"]


def test_red_flag_meningitis_emergency(client):
    """Test emergency classification for fever with stiff neck."""
    payload = {
        "symptoms": ["stiff neck with fever", "severe headache", "nausea"],
        "age": 22,
        "sex": "male",
        "duration_days": 1,
        "severity_scale": 8
    }
    response = client.post("/api/v1/triage/check", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["urgency"] == "emergency"
    assert len(data["red_flags_triggered"]) >= 1


def test_mild_symptom_self_care(client):
    """Test self-care classification for mild viral symptoms."""
    payload = {
        "symptoms": ["nasal congestion", "runny nose", "fatigue"],
        "age": 25,
        "sex": "female",
        "duration_days": 2,
        "severity_scale": 3
    }
    response = client.post("/api/v1/triage/check", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["urgency"] == "self_care"
    assert len(data["red_flags_triggered"]) == 0
    assert len(data["possible_conditions"]) >= 1
    top_cond = data["possible_conditions"][0]
    assert top_cond["condition_code"] in ["cond_common_cold", "cond_allergic_rhinitis"]


def test_triage_history_persistence(client, patient_headers):
    """Test saving and retrieving triage history for an authenticated patient."""
    payload = {
        "symptoms": ["headache", "fatigue"],
        "age": 28,
        "sex": "female",
        "duration_days": 2,
        "severity_scale": 4
    }
    # 1. Run check as authenticated patient
    res = client.post("/api/v1/triage/check", json=payload, headers=patient_headers)
    assert res.status_code == 200
    session_id = res.json()["session_id"]
    assert session_id is not None

    # 2. Fetch history
    hist_res = client.get("/api/v1/triage/history", headers=patient_headers)
    assert hist_res.status_code == 200
    history = hist_res.json()
    assert len(history) >= 1
    assert any(h["id"] == session_id for h in history)

    # 3. Fetch single session detail
    detail_res = client.get(f"/api/v1/triage/sessions/{session_id}", headers=patient_headers)
    assert detail_res.status_code == 200
    assert detail_res.json()["id"] == session_id
