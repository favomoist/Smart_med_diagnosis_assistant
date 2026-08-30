def test_public_symptoms_catalog(client):
    response = client.get("/api/v1/knowledge/symptoms")
    assert response.status_code == 200
    symptoms = response.json()
    assert len(symptoms) >= 10
    codes = [s["code"] for s in symptoms]
    assert "chest_pain" in codes
    assert "fever" in codes


def test_symptom_search(client):
    response = client.get("/api/v1/knowledge/symptoms?search=cough")
    assert response.status_code == 200
    results = response.json()
    assert len(results) >= 1
    assert any("cough" in s["name"].lower() for s in results)


def test_public_conditions_catalog(client):
    response = client.get("/api/v1/knowledge/conditions")
    assert response.status_code == 200
    conditions = response.json()
    assert len(conditions) >= 5
    codes = [c["code"] for c in conditions]
    assert "cond_mi" in codes
    assert "cond_common_cold" in codes


def test_admin_create_symptom_permission(client, patient_headers, admin_headers):
    payload = {
        "code": "new_symptom_test",
        "name": "New Test Symptom",
        "category": "General",
        "description": "A test symptom for RBAC validation",
        "is_red_flag": False,
        "guidance": "Test guidance"
    }
    # Patient should be rejected (403 Forbidden)
    forbidden_res = client.post("/api/v1/knowledge/symptoms", json=payload, headers=patient_headers)
    assert forbidden_res.status_code == 403

    # Admin should succeed (201 Created)
    admin_res = client.post("/api/v1/knowledge/symptoms", json=payload, headers=admin_headers)
    assert admin_res.status_code == 201
    assert admin_res.json()["code"] == "new_symptom_test"
