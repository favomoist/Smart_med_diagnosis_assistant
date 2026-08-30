def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"


def test_user_registration(client):
    payload = {
        "email": "brandnewuser@example.com",
        "password": "strongpassword123",
        "full_name": "New User",
        "role": "patient"
    }
    response = client.post("/api/v1/auth/register", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert data["role"] == "patient"
    assert data["full_name"] == "New User"


def test_user_registration_duplicate(client):
    payload = {
        "email": "duplicate_check@example.com",
        "password": "password123",
        "full_name": "Original User",
        "role": "patient"
    }
    first_res = client.post("/api/v1/auth/register", json=payload)
    assert first_res.status_code == 201

    # Second attempt with same email
    dup_res = client.post("/api/v1/auth/register", json=payload)
    assert dup_res.status_code == 400
    assert "already exists" in dup_res.json()["detail"]


def test_user_login_success(client, test_patient_user):
    payload = {
        "email": test_patient_user.email,
        "password": "patientpassword123"
    }
    response = client.post("/api/v1/auth/login", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["user_id"] == test_patient_user.id


def test_user_login_invalid_password(client, test_patient_user):
    payload = {
        "email": test_patient_user.email,
        "password": "wrongpassword"
    }
    response = client.post("/api/v1/auth/login", json=payload)
    assert response.status_code == 401
    assert "Invalid email or password" in response.json()["detail"]


def test_get_current_user(client, patient_headers):
    response = client.get("/api/v1/auth/me", headers=patient_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "patient@example.com"
    assert data["full_name"] == "Priya Patient"


def test_profile_crud_and_dependent_management(client, patient_headers):
    # 1. List initial profiles (should have default 'self' profile)
    res = client.get("/api/v1/profiles", headers=patient_headers)
    assert res.status_code == 200
    profiles = res.json()
    assert len(profiles) >= 1
    self_profile = profiles[0]
    assert self_profile["relationship"] == "self"

    # 2. Add dependent profile (Caregiver scenario - US-11)
    dep_payload = {
        "name": "Grandpa Joe",
        "relationship": "parent",
        "age": 78,
        "sex": "male",
        "known_allergies": "Penicillin",
        "chronic_conditions": "Hypertension"
    }
    create_res = client.post("/api/v1/profiles", json=dep_payload, headers=patient_headers)
    assert create_res.status_code == 201
    dep_data = create_res.json()
    assert dep_data["name"] == "Grandpa Joe"
    assert dep_data["relationship"] == "parent"
    dep_id = dep_data["id"]

    # 3. Update dependent profile (US-10)
    update_res = client.put(f"/api/v1/profiles/{dep_id}", json={"age": 79}, headers=patient_headers)
    assert update_res.status_code == 200
    assert update_res.json()["age"] == 79

    # 4. Delete dependent profile
    del_res = client.delete(f"/api/v1/profiles/{dep_id}", headers=patient_headers)
    assert del_res.status_code == 204
