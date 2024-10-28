from fastapi.testclient import TestClient
from src.main import app  # Замініть на ваш файл основного додатку
from src.comments.schemas import CommentCreate, CommentUpdate

client = TestClient(app)


def test_create_comment():
    response = client.post(
        "/auth/register",
        json={"email": "test@example.com", "password": "password123", "username": "testuser"}
    )
    tokens = response.json()
    access_token = tokens["access_token"]

    create_post_response = client.post(
        "/api/post",
        headers={"Authorization": f"Bearer {access_token}"},
        json={"content": "This is a test post", "title": "Test Title"}
    )
    post_id = create_post_response.json()["id"]

    response = client.post(
        f"/api/post/{post_id}/comment",
        headers={"Authorization": f"Bearer {access_token}"},
        json={"content": "This is a test comment"}
    )
    assert response.status_code == 200
    assert "id" in response.json()


def test_get_comment():
    response = client.post(
        "/auth/register",
        json={"email": "test@example.com", "password": "password123", "username": "testuser"}
    )
    tokens = response.json()
    access_token = tokens["access_token"]

    create_post_response = client.post(
        "/api/post",
        headers={"Authorization": f"Bearer {access_token}"},
        json={"content": "This is a test post", "title": "Test Title"}
    )
    post_id = create_post_response.json()["id"]

    create_comment_response = client.post(
        f"/api/post/{post_id}/comment",
        headers={"Authorization": f"Bearer {access_token}"},
        json={"content": "This is a test comment"}
    )
    comment_id = create_comment_response.json()["id"]

    response = client.get(f"/api/comment/{comment_id}")
    assert response.status_code == 200
    assert response.json()["id"] == comment_id


def test_get_comments_for_post():
    response = client.post(
        "/auth/register",
        json={"email": "test@example.com", "password": "password123", "username": "testuser"}
    )
    tokens = response.json()
    access_token = tokens["access_token"]

    create_post_response = client.post(
        "/api/post",
        headers={"Authorization": f"Bearer {access_token}"},
        json={"content": "This is a test post", "title": "Test Title"}
    )
    post_id = create_post_response.json()["id"]

    client.post(
        f"/api/post/{post_id}/comment",
        headers={"Authorization": f"Bearer {access_token}"},
        json={"content": "First comment"}
    )
    client.post(
        f"/api/post/{post_id}/comment",
        headers={"Authorization": f"Bearer {access_token}"},
        json={"content": "Second comment"}
    )

    response = client.get(f"/api/post/{post_id}/comments")
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_update_comment():
    response = client.post(
        "/auth/register",
        json={"email": "test@example.com", "password": "password123", "username": "testuser"}
    )
    tokens = response.json()
    access_token = tokens["access_token"]

    create_post_response = client.post(
        "/api/post",
        headers={"Authorization": f"Bearer {access_token}"},
        json={"content": "This is a test post", "title": "Test Title"}
    )
    post_id = create_post_response.json()["id"]

    create_comment_response = client.post(
        f"/api/post/{post_id}/comment",
        headers={"Authorization": f"Bearer {access_token}"},
        json={"content": "This is a test comment"}
    )
    comment_id = create_comment_response.json()["id"]

    update_response = client.patch(
        f"/api/comment/{comment_id}",
        headers={"Authorization": f"Bearer {access_token}"},
        json={"content": "Updated comment"}
    )
    assert update_response.status_code == 200
    assert update_response.json()["content"] == "Updated comment"


def test_delete_comment():
    response = client.post(
        "/auth/register",
        json={"email": "test@example.com", "password": "password123", "username": "testuser"}
    )
    tokens = response.json()
    access_token = tokens["access_token"]

    create_post_response = client.post(
        "/api/post",
        headers={"Authorization": f"Bearer {access_token}"},
        json={"content": "This is a test post", "title": "Test Title"}
    )
    post_id = create_post_response.json()["id"]

    create_comment_response = client.post(
        f"/api/post/{post_id}/comment",
        headers={"Authorization": f"Bearer {access_token}"},
        json={"content": "This is a test comment"}
    )
    comment_id = create_comment_response.json()["id"]

    delete_response = client.delete(f"/api/comment/{comment_id}", headers={"Authorization": f"Bearer {access_token}"})
    assert delete_response.status_code == 204

    get_response = client.get(f"/api/comment/{comment_id}")
    assert get_response.status_code == 404
