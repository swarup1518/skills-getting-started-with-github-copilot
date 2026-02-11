import copy

from fastapi.testclient import TestClient

from src.app import app, activities


client = TestClient(app)
_original_activities = copy.deepcopy(activities)


def reset_activities():
    activities.clear()
    activities.update(copy.deepcopy(_original_activities))


def test_get_activities():
    reset_activities()
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert "Soccer Club" in data
    assert isinstance(data["Soccer Club"]["participants"], list)


def test_signup_success():
    reset_activities()
    response = client.post("/activities/Chess%20Club/signup", params={"email": "new@mergington.edu"})
    assert response.status_code == 200
    assert "new@mergington.edu" in activities["Chess Club"]["participants"]


def test_signup_duplicate_rejected():
    reset_activities()
    response = client.post("/activities/Chess%20Club/signup", params={"email": "michael@mergington.edu"})
    assert response.status_code == 400


def test_remove_participant():
    reset_activities()
    response = client.delete(
        "/activities/Chess%20Club/participants",
        params={"email": "michael@mergington.edu"},
    )
    assert response.status_code == 200
    assert "michael@mergington.edu" not in activities["Chess Club"]["participants"]
