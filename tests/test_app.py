import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

# Test: GET /activities
# AAA: Arrange-Act-Assert

def test_get_activities():
    # Arrange: (nothing to arrange for this test)
    # Act
    response = client.get("/activities")
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data


def test_signup_success():
    # Arrange
    email = "testuser1@mergington.edu"
    activity = "Chess Club"
    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")
    # Assert
    assert response.status_code == 200
    assert f"Signed up {email} for {activity}" in response.json()["message"]
    # Cleanup
    client.delete(f"/activities/{activity}/participants/{email}")


def test_signup_duplicate():
    # Arrange
    email = "testuser2@mergington.edu"
    activity = "Chess Club"
    # Act
    client.post(f"/activities/{activity}/signup?email={email}")
    response = client.post(f"/activities/{activity}/signup?email={email}")
    # Assert
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]
    # Cleanup
    client.delete(f"/activities/{activity}/participants/{email}")


def test_remove_participant():
    # Arrange
    email = "testuser3@mergington.edu"
    activity = "Chess Club"
    client.post(f"/activities/{activity}/signup?email={email}")
    # Act
    response = client.delete(f"/activities/{activity}/participants/{email}")
    # Assert
    assert response.status_code == 200
    assert f"Removed {email} from {activity}" in response.json()["message"]


def test_remove_nonexistent_participant():
    # Arrange
    email = "notfound@mergington.edu"
    activity = "Chess Club"
    # Act
    response = client.delete(f"/activities/{activity}/participants/{email}")
    # Assert
    assert response.status_code == 404
    assert "Participant not found" in response.json()["detail"]
