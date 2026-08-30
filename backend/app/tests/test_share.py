def test_create_and_view_shared_summary(client, patient_headers, clinician_headers):
    # 1. Create a triage session first
    check_payload = {
        "symptoms": ["cough", "sore throat", "fever"],
        "age": 28,
        "sex": "female",
        "duration_days": 3,
        "severity_scale": 5
    }
    check_res = client.post("/api/v1/triage/check", json=check_payload, headers=patient_headers)
    assert check_res.status_code == 200
    session_id = check_res.json()["session_id"]
    assert session_id is not None

    # 2. Generate shareable token
    share_payload = {
        "session_id": session_id,
        "valid_hours": 48
    }
    share_res = client.post("/api/v1/share/create", json=share_payload, headers=patient_headers)
    assert share_res.status_code == 201
    share_data = share_res.json()
    token = share_data["token"]
    assert token is not None
    assert "/api/v1/share/" in share_data["share_url"]

    # 3. Access summary via public link / token (no auth required)
    view_res = client.get(f"/api/v1/share/{token}")
    assert view_res.status_code == 200
    view_data = view_res.json()
    assert view_data["token"] == token
    assert view_data["session_details"]["id"] == session_id
    assert "cough" in view_data["session_details"]["reported_symptoms"]

    # 4. Patient tries to add clinician note (should be 403 Forbidden)
    note_payload = {"notes": "Patient trying to write clinician note"}
    bad_note_res = client.post(f"/api/v1/share/{token}/notes", json=note_payload, headers=patient_headers)
    assert bad_note_res.status_code == 403

    # 5. Clinician adds consultation notes (should be 200 OK)
    clinician_note = {"notes": "Patient presents with viral URTI symptoms. Recommended hydration and symptom monitoring."}
    good_note_res = client.post(f"/api/v1/share/{token}/notes", json=clinician_note, headers=clinician_headers)
    assert good_note_res.status_code == 200
    assert good_note_res.json()["clinician_notes"] == clinician_note["notes"]
