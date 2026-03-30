import pytest

# All tests use the Arrange-Act-Assert (AAA) pattern

def test_get_activities(client):
    # Arrange: (client fixture provides TestClient, activities pre-populated)
    # Act
    response = client.get("/activities")
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data

def test_signup_success(client):
    # Arrange
    email = "student@example.com"
    activity = "Chess Club"
    # Act
    response = client.post(f"/activities/{activity}/signup", json={"email": email})
    # Assert
    assert response.status_code == 200
    assert response.json()["message"].startswith("Signed up")


def test_signup_duplicate(client):
    # Arrange
    email = "student@example.com"
    activity = "Chess Club"
    client.post(f"/activities/{activity}/signup", json={"email": email})
    # Act
    response = client.post(f"/activities/{activity}/signup", json={"email": email})
    # Assert
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]


def test_signup_nonexistent_activity(client):
    # Arrange
    email = "student@example.com"
    activity = "Nonexistent Club"
    # Act
    response = client.post(f"/activities/{activity}/signup", json={"email": email})
    # Assert
    assert response.status_code == 404
    assert "not found" in response.json()["detail"]


def test_unregister_success(client):
    # Arrange
    email = "student@example.com"
    activity = "Chess Club"
    client.post(f"/activities/{activity}/signup", json={"email": email})
    # Act
    response = client.post(f"/activities/{activity}/unregister", json={"email": email})
    # Assert
    assert response.status_code == 200
    assert response.json()["message"].startswith("Unregistered")


def test_unregister_not_enrolled(client):
    # Arrange
    email = "student@example.com"
    activity = "Chess Club"
    # Act
    response = client.post(f"/activities/{activity}/unregister", json={"email": email})
    # Assert
    assert response.status_code == 404
    assert "not enrolled" in response.json()["detail"]


def test_unregister_nonexistent_activity(client):
    # Arrange
    email = "student@example.com"
    activity = "Nonexistent Club"
    # Act
    response = client.post(f"/activities/{activity}/unregister", json={"email": email})
    # Assert
    assert response.status_code == 404
    assert "not found" in response.json()["detail"]
