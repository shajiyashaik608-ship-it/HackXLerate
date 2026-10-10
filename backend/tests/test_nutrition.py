from datetime import date


def test_nutrition_meals_and_recommendations(client, auth_headers):
    # Search all meals
    res = client.get("/api/v1/nutrition/meals", headers=auth_headers)
    assert res.status_code == 200
    meals = res.json()
    assert len(meals) > 0

    # Filter by breakfast & veg
    filter_res = client.get("/api/v1/nutrition/meals?category=breakfast&diet_type=veg", headers=auth_headers)
    assert filter_res.status_code == 200
    filtered = filter_res.json()
    assert all(m["category"] == "breakfast" for m in filtered)

    # Recommendations
    rec_res = client.get("/api/v1/nutrition/recommend?diet_type=veg", headers=auth_headers)
    assert rec_res.status_code == 200
    data = rec_res.json()
    assert "breakfast" in data
    assert "lunch" in data
    assert "dinner" in data
    assert "educational_guidance" in data


def test_meal_plan_flow(client, auth_headers):
    # Fetch first available meal item ID
    meals_res = client.get("/api/v1/nutrition/meals", headers=auth_headers)
    meal_id = meals_res.json()[0]["id"]

    today = date.today().isoformat()
    plan_payload = {
        "plan_date": today,
        "items": [
            {"meal_item_id": meal_id, "meal_slot": "breakfast", "servings": 1.0}
        ]
    }
    create_res = client.post("/api/v1/nutrition/plan", json=plan_payload, headers=auth_headers)
    assert create_res.status_code == 201
    plan_data = create_res.json()
    assert plan_data["plan_date"] == today
    assert len(plan_data["items"]) == 1
    plan_id = plan_data["id"]

    # Retrieve plan
    get_res = client.get(f"/api/v1/nutrition/plan?plan_date={today}", headers=auth_headers)
    assert get_res.status_code == 200
    assert get_res.json()["id"] == plan_id

    # Delete plan
    del_res = client.delete(f"/api/v1/nutrition/plan/{plan_id}", headers=auth_headers)
    assert del_res.status_code == 200
