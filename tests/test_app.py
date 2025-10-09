import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert len(data) > 0
    for activity, details in data.items():
        assert "description" in details
        assert "schedule" in details
        assert "max_participants" in details
        assert "participants" in details

def test_signup_and_duplicate():
    # Use a unique email for testing
    test_email = "pytestuser@mergington.edu"
    activity = list(client.get("/activities").json().keys())[0]
    # First signup should succeed
    resp1 = client.post(f"/activities/{activity}/signup?email={test_email}")
    assert resp1.status_code == 200
    # Duplicate signup should fail
    resp2 = client.post(f"/activities/{activity}/signup?email={test_email}")
    assert resp2.status_code == 400

def test_unregister():
    test_email = "pytestuser2@mergington.edu"
    activity = list(client.get("/activities").json().keys())[0]
    # Register first
    client.post(f"/activities/{activity}/signup?email={test_email}")
    # Unregister
    resp = client.post(f"/activities/{activity}/unregister?email={test_email}")
    assert resp.status_code == 200
    # Unregister again should fail
    resp2 = client.post(f"/activities/{activity}/unregister?email={test_email}")
    assert resp2.status_code == 400
