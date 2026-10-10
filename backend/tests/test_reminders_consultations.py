def test_reminder_lifecycle(client, auth_headers):
    # Create reminder
    payload = {
        "title": "Myo-Inositol Supplement",
        "category": "medication",
        "scheduled_time": "08:30",
        "recurrence": "daily",
        "notes": "With morning breakfast"
    }
    create_res = client.post("/api/v1/reminders", json=payload, headers=auth_headers)
    assert create_res.status_code == 201
    rem_id = create_res.json()["id"]

    # List reminders
    list_res = client.get("/api/v1/reminders", headers=auth_headers)
    assert list_res.status_code == 200
    assert any(r["id"] == rem_id for r in list_res.json())

    # Complete reminder
    comp_res = client.post(f"/api/v1/reminders/{rem_id}/complete", headers=auth_headers)
    assert comp_res.status_code == 200
    assert comp_res.json()["is_completed"] is True

    # Snooze reminder
    snooze_res = client.post(f"/api/v1/reminders/{rem_id}/snooze", json={"snooze_minutes": 45}, headers=auth_headers)
    assert snooze_res.status_code == 200
    assert snooze_res.json()["is_completed"] is False
    assert snooze_res.json()["snoozed_until"] is not None

    # Delete reminder
    del_res = client.delete(f"/api/v1/reminders/{rem_id}", headers=auth_headers)
    assert del_res.status_code == 200


def test_consultation_brief_lifecycle(client, auth_headers):
    # Generate brief
    payload = {
        "primary_concerns": "Irregular cycles and fatigue",
        "symptoms_summary": "Acne and mild bloating",
        "prioritized_questions": "Should I repeat my TSH test?"
    }
    create_res = client.post("/api/v1/consultations/brief", json=payload, headers=auth_headers)
    assert create_res.status_code == 201
    brief_data = create_res.json()
    assert brief_data["primary_concerns"] == "Irregular cycles and fatigue"
    brief_id = brief_data["id"]

    # Fetch brief details
    get_res = client.get(f"/api/v1/consultations/briefs/{brief_id}", headers=auth_headers)
    assert get_res.status_code == 200
    assert get_res.json()["id"] == brief_id

    # Update brief
    patch_res = client.patch(
        f"/api/v1/consultations/briefs/{brief_id}",
        json={"primary_concerns": "Updated: Irregular cycles"},
        headers=auth_headers
    )
    assert patch_res.status_code == 200
    assert patch_res.json()["primary_concerns"] == "Updated: Irregular cycles"

    # Delete brief
    del_res = client.delete(f"/api/v1/consultations/briefs/{brief_id}", headers=auth_headers)
    assert del_res.status_code == 200
