import sys, os
import pytest
from fastapi.testclient import TestClient

# Add backend and ai-ml to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../backend")))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../ai-ml")))

from app.main import app

client = TestClient(app)

def test_health_check_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "online"
    assert data["service"] == "Health Saathi API"
    assert "safety_guardrails" in data

def test_food_recommendations_endpoint():
    response = client.get("/api/v1/food/recommendations?diet_type=vegetarian")
    assert response.status_code == 200
    data = response.json()
    assert "recommendations" in data
    assert len(data["recommendations"]) > 0
    assert "disclaimer" in data

def test_telugu_assistant_chat_endpoint():
    payload = {
        "question": "PCOS ante enti?",
        "language": "te"
    }
    response = client.post("/api/v1/assistant/chat", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["language"] == "te"
    assert "పిసిఒఎస్" in data["answer"]
    assert "గమనిక" in data["answer"]
