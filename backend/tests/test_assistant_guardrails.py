def test_assistant_chat_english(client, auth_headers):
    payload = {
        "message": "What is PCOS and what foods help?",
        "language": "en"
    }
    res = client.post("/api/v1/assistant/chat", json=payload, headers=auth_headers)
    assert res.status_code == 200
    data = res.json()
    assert "answer" in data
    assert data["language"] == "en"
    assert data["urgent_care_flag"] is False
    assert len(data["sources"]) > 0
    assert data["is_mock_response"] is True


def test_assistant_chat_telugu(client, auth_headers):
    payload = {
        "message": "పీసీఓఎస్ అంటే ఏమిటి? ఆహారం ఎలా ఉండాలి?",
        "language": "te"
    }
    res = client.post("/api/v1/assistant/chat", json=payload, headers=auth_headers)
    assert res.status_code == 200
    data = res.json()
    assert "answer" in data
    assert data["language"] == "te"
    assert data["urgent_care_flag"] is False


def test_emergency_red_flag_detection(client, auth_headers):
    # Query reporting acute severe pelvic pain
    payload = {
        "message": "I have severe pelvic pain and sudden heavy bleeding",
        "language": "en"
    }
    res = client.post("/api/v1/assistant/chat", json=payload, headers=auth_headers)
    assert res.status_code == 200
    data = res.json()
    assert data["urgent_care_flag"] is True
    assert "URGENT MEDICAL ADVICE" in data["answer"]


def test_conversations_listing_and_deletion(client, auth_headers):
    # Post a message first to establish conversation
    client.post("/api/v1/assistant/chat", json={"message": "Hello Health Saathi", "language": "en"}, headers=auth_headers)

    conv_res = client.get("/api/v1/assistant/conversations", headers=auth_headers)
    assert conv_res.status_code == 200
    conv_list = conv_res.json()
    assert len(conv_list) >= 1
    conv_id = conv_list[0]["id"]

    # Delete conversation
    del_res = client.delete(f"/api/v1/assistant/conversations/{conv_id}", headers=auth_headers)
    assert del_res.status_code == 200
