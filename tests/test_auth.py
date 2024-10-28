from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)


def test_register_user():
    response = client.post(
        "/auth/register",
        json={"email": "test@example.com", "password": "password123", "username": "testuser"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert "refresh_token" in response.json()


def test_login_user():
    client.post(
        "/auth/register",
        json={"email": "test@example.com", "password": "password123", "username": "testuser"}
    )

    response = client.post(
        "/auth/token",
        data={"username": "test@example.com", "password": "password123"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert "refresh_token" in response.json()


def test_login_invalid_user():
    response = client.post(
        "/auth/token",
        data={"username": "nonexistent@example.com", "password": "wrongpassword"}
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect email or password"


def test_get_current_user():
    response = client.post(
        "/auth/register",
        json={"email": "test@example.com", "password": "password123", "username": "testuser"}
    )
    tokens = response.json()
    access_token = tokens["access_token"]

    response = client.get("/auth/me", headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == 200
    assert response.json()["email"] == "test@example.com"
