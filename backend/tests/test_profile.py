def test_get_and_update_health_profile(client, auth_headers):
    # Get profile
    res = client.get("/api/v1/profile", headers=auth_headers)
    assert res.status_code == 200
    data = res.json()
    assert data["diet_type"] == "veg"

    # Update profile
    payload = {
        "age": 27,
        "diet_type": "egg",
        "baseline_cycle_length": 35,
        "wellness_goals": "Insulin sensitivity and regular cycles"
    }
    update_res = client.patch("/api/v1/profile", json=payload, headers=auth_headers)
    assert update_res.status_code == 200
    updated = update_res.json()
    assert updated["age"] == 27
    assert updated["diet_type"] == "egg"
    assert updated["baseline_cycle_length"] == 35
