from fastapi.testclient import TestClient
from src.main import app
from src.posts.schemas import PostCreate, PostUpdate

client = TestClient(app)


def test_create_post():
    response = client.post(
        "/auth/register",
        json={"email": "test@example.com", "password": "password123", "username": "testuser"}
    )
    tokens = response.json()
    access_token = tokens["access_token"]

    response = client.post(
        "/api/post",
        headers={"Authorization": f"Bearer {access_token}"},
        json={"content": "This is a test post", "title": "Test Title"}
    )
    assert response.status_code == 200
    assert "id" in response.json()


def test_get_post():
    response = client.post(
        "/auth/register",
        json={"email": "test@example.com", "password": "password123", "username": "testuser"}
    )
    tokens = response.json()
    access_token = tokens["access_token"]

    create_response = client.post(
        "/api/post",
        headers={"Authorization": f"Bearer {access_token}"},
        json={"content": "This is a test post", "title": "Test Title"}
    )
    post_id = create_response.json()["id"]

    response = client.get(f"/api/post/{post_id}")
    assert response.status_code == 200
    assert response.json()["id"] == post_id


def test_update_post():
    response = client.post(
        "/auth/register",
        json={"email": "test@example.com", "password": "password123", "username": "testuser"}
    )
    tokens = response.json()
    access_token = tokens["access_token"]

    create_response = client.post(
        "/api/post",
        headers={"Authorization": f"Bearer {access_token}"},
        json={"content": "This is a test post", "title": "Test Title"}
    )
    post_id = create_response.json()["id"]

    update_response = client.patch(
        f"/api/post/{post_id}",
        headers={"Authorization": f"Bearer {access_token}"},
        json={"content": "Updated post content"}
    )
    assert update_response.status_code == 200
    assert update_response.json()["content"] == "Updated post content"


def test_delete_post():
    response = client.post(
        "/auth/register",
        json={"email": "test@example.com", "password": "password123", "username": "testuser"}
    )
    tokens = response.json()
    access_token = tokens["access_token"]

    create_response = client.post(
        "/api/post",
        headers={"Authorization": f"Bearer {access_token}"},
        json={"content": "This is a test post", "title": "Test Title"}
    )
    post_id = create_response.json()["id"]

    delete_response = client.delete(f"/api/post/{post_id}", headers={"Authorization": f"Bearer {access_token}"})
    assert delete_response.status_code == 204

    get_response = client.get(f"/api/post/{post_id}")
    assert get_response.status_code == 404
