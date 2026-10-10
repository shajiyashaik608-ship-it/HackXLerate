from datetime import date, timedelta


def test_cycle_logging_and_validation(client, auth_headers):
    today = date.today()
    # Valid cycle
    payload = {
        "start_date": (today - timedelta(days=20)).isoformat(),
        "end_date": (today - timedelta(days=15)).isoformat(),
        "flow_intensity": "medium",
        "notes": "Normal cycle"
    }
    res = client.post("/api/v1/cycles/log", json=payload, headers=auth_headers)
    assert res.status_code == 201
    assert res.json()["duration_days"] == 6

    # Invalid cycle (end before start)
    invalid_payload = {
        "start_date": today.isoformat(),
        "end_date": (today - timedelta(days=2)).isoformat(),
        "flow_intensity": "medium"
    }
    inv_res = client.post("/api/v1/cycles/log", json=invalid_payload, headers=auth_headers)
    assert inv_res.status_code in [400, 422]


def test_cycle_estimation_workflow(client, auth_headers):
    # Check estimate before logging cycles
    est_res = client.get("/api/v1/cycles/estimate", headers=auth_headers)
    assert est_res.status_code == 200

    # Log 3 cycles with varying intervals (35 days, 33 days)
    today = date.today()
    dates = [
        (today - timedelta(days=70), today - timedelta(days=66)),
        (today - timedelta(days=35), today - timedelta(days=31)),
        (today - timedelta(days=2), today + timedelta(days=2))
    ]
    for s_date, e_date in dates:
        client.post("/api/v1/cycles/log", json={
            "start_date": s_date.isoformat(),
            "end_date": e_date.isoformat(),
            "flow_intensity": "medium"
        }, headers=auth_headers)

    # Re-evaluate estimate with sufficient history
    est_res2 = client.get("/api/v1/cycles/estimate", headers=auth_headers)
    assert est_res2.status_code == 200
    data = est_res2.json()
    assert data["has_sufficient_history"] is True
    assert len(data["historical_intervals"]) >= 2
    assert "estimated_arrival_window" in data
    assert "uncertainty_notice" in data


def test_symptom_logging_and_summary(client, auth_headers):
    today = date.today()
    client.post("/api/v1/symptoms/log", json={
        "recorded_date": today.isoformat(),
        "symptom_type": "acne",
        "severity": "mild",
        "notes": "Mild chin breakout"
    }, headers=auth_headers)

    client.post("/api/v1/symptoms/log", json={
        "recorded_date": today.isoformat(),
        "symptom_type": "cramps",
        "severity": "moderate",
        "notes": "Day 1 cramps"
    }, headers=auth_headers)

    # History
    hist_res = client.get("/api/v1/symptoms/history", headers=auth_headers)
    assert hist_res.status_code == 200
    assert len(hist_res.json()) >= 2

    # Summary
    summary_res = client.get("/api/v1/symptoms/summary", headers=auth_headers)
    assert summary_res.status_code == 200
    assert summary_res.json()["total_entries"] >= 2
    assert len(summary_res.json()["symptoms"]) >= 2
