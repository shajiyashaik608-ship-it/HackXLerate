def test_community_post_and_replies(client, auth_headers):
    # Create post
    payload = {
        "title": "Millets vs White Rice",
        "content": "Switching to Foxtail millet helped my mid-day satiety.",
        "pseudonym": "HyderabadSaathi",
        "tags": "nutrition,millets"
    }
    create_res = client.post("/api/v1/community/posts", json=payload, headers=auth_headers)
    assert create_res.status_code == 201
    post_data = create_res.json()
    assert post_data["pseudonym"] == "HyderabadSaathi"
    assert "user_id" not in post_data  # Privacy check: private IDs not exposed
    post_id = post_data["id"]

    # Public list posts
    list_res = client.get("/api/v1/community/posts")
    assert list_res.status_code == 200
    assert any(p["id"] == post_id for p in list_res.json())

    # Add reply
    reply_payload = {
        "content": "I agree! Ragi idlis also work wonderfully for me.",
        "pseudonym": "PCOS_Friend"
    }
    reply_res = client.post(f"/api/v1/community/posts/{post_id}/replies", json=reply_payload, headers=auth_headers)
    assert reply_res.status_code == 201
    assert reply_res.json()["pseudonym"] == "PCOS_Friend"

    # Report post
    report_res = client.post(
        f"/api/v1/community/posts/{post_id}/report",
        json={"reason": "Testing moderation report workflow"},
        headers=auth_headers
    )
    assert report_res.status_code == 200
    assert report_res.json()["status"] == "pending_review"

    # Vote on post
    vote_res = client.post(f"/api/v1/community/posts/{post_id}/vote")
    assert vote_res.status_code == 200
    assert vote_res.json()["success"] is True
