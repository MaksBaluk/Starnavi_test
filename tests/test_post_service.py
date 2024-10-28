import pytest
from fastapi import HTTPException
from sqlalchemy.orm import Session
from src.posts.models import Post
from src.posts.schemas import PostCreate, PostUpdate
from src.posts.services import PostService
from src.utils.moderation import is_toxic_content


@pytest.fixture
def post_service(db_session: Session):
    return PostService(db_session)


def test_create_post(post_service: PostService):
    post_data = PostCreate(content="This is a test post", title="Test Title")
    owner_id = 1

    new_post = post_service.create_post(post_data, owner_id)

    assert new_post.content == post_data.content
    assert new_post.title == post_data.title
    assert new_post.owner_id == owner_id


def test_create_post_with_toxic_content(post_service: PostService):
    post_data = PostCreate(content="Toxic content example", title="Test Title")

    with pytest.raises(HTTPException) as exc_info:
        post_service.create_post(post_data, owner_id=1)
    assert exc_info.value.status_code == 400
    assert str(exc_info.value.detail) == "Post contains toxic content and cannot be created."


def test_get_post_by_id(post_service: PostService):
    post_data = PostCreate(content="Test post content", title="Test Title")
    owner_id = 1
    post_service.create_post(post_data, owner_id)

    post = post_service.get_post_by_id(1)
    assert post is not None
    assert post.id == 1


def test_update_post(post_service: PostService):
    post_data = PostCreate(content="Original content", title="Original Title")
    owner_id = 1
    post = post_service.create_post(post_data, owner_id)

    update_data = PostUpdate(content="Updated content")
    updated_post = post_service.update_post_crud(post.id, update_data)

    assert updated_post.content == "Updated content"
    assert updated_post.title == post.title


def test_delete_post(post_service: PostService):
    post_data = PostCreate(content="Test post to delete", title="Test Title")
    owner_id = 1
    post = post_service.create_post(post_data, owner_id)

    post_service.delete_post_crud(post.id)

    with pytest.raises(HTTPException):
        post_service.get_post_by_id(post.id)
