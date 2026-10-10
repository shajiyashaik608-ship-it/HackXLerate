def test_privacy_export(client, auth_headers, test_user):
    res = client.get("/api/v1/privacy/export", headers=auth_headers)
    assert res.status_code == 200
    data = res.json()
    assert data["export_version"] == "1.0"
    assert data["user_info"]["email"] == test_user.email
    assert "health_profile" in data
    assert "medical_documents" in data
    assert "biomarkers" in data
    assert "cycle_records" in data


def test_privacy_purge_invalid_phrase_fails(client, auth_headers):
    res = client.post(
        "/api/v1/privacy/purge",
        json={"confirm_phrase": "wrong phrase"},
        headers=auth_headers
    )
    assert res.status_code in [400, 422]


def test_privacy_purge_success(client, auth_headers, test_user):
    # Execute full purge
    res = client.post(
        "/api/v1/privacy/purge",
        json={"confirm_phrase": "DELETE MY HEALTH DATA"},
        headers=auth_headers
    )
    assert res.status_code == 200
    assert res.json()["status"] == "completed"

    # Verify user account no longer exists
    get_me = client.get("/api/v1/auth/me", headers=auth_headers)
    assert get_me.status_code == 401
