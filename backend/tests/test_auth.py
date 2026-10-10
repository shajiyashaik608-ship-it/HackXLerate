def test_signup_successful(client):
    payload = {
        "email": "new_patient@healthsaathi.in",
        "password": "SecurePassword123!",
        "full_name": "New Patient",
        "preferred_language": "en",
        "consent_given": True
    }
    response = client.post("/api/v1/auth/signup", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["user"]["email"] == "new_patient@healthsaathi.in"
    assert data["user"]["full_name"] == "New Patient"


def test_signup_duplicate_email_fails(client, test_user):
    payload = {
        "email": test_user.email,
        "password": "AnotherPassword123!",
        "full_name": "Duplicate User",
        "consent_given": True
    }
    response = client.post("/api/v1/auth/signup", json=payload)
    assert response.status_code in [400, 422]


def test_login_success(client, test_user):
    payload = {
        "email": test_user.email,
        "password": "StrongTestPass123!"
    }
    response = client.post("/api/v1/auth/login", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["user"]["email"] == test_user.email


def test_login_invalid_password(client, test_user):
    payload = {
        "email": test_user.email,
        "password": "IncorrectPassword!"
    }
    response = client.post("/api/v1/auth/login", json=payload)
    assert response.status_code == 401


def test_refresh_token(client, test_user):
    # First login to get refresh token
    login_res = client.post("/api/v1/auth/login", json={
        "email": test_user.email,
        "password": "StrongTestPass123!"
    })
    refresh_token = login_res.json()["refresh_token"]

    response = client.post("/api/v1/auth/refresh", json={"refresh_token": refresh_token})
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_protected_route_without_token_fails(client):
    response = client.get("/api/v1/auth/me")
    assert response.status_code == 401


def test_protected_route_with_token(client, auth_headers, test_user):
    response = client.get("/api/v1/auth/me", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["email"] == test_user.email


def test_user_settings_and_consent(client, auth_headers):
    # Update settings
    res = client.patch("/api/v1/users/settings", json={"full_name": "Updated Name"}, headers=auth_headers)
    assert res.status_code == 200
    assert res.json()["full_name"] == "Updated Name"

    # Update consent
    res2 = client.post("/api/v1/users/consent", json={"consent_given": False}, headers=auth_headers)
    assert res2.status_code == 200
    assert res2.json()["consent_given"] is False
