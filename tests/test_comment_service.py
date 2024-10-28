import pytest
from fastapi import HTTPException
from sqlalchemy.orm import Session
from src.posts.models import Post
from src.comments.schemas import CommentCreate, CommentUpdate
from src.comments.services import CommentService
from src.utils.moderation import is_toxic_content




@pytest.fixture
def comment_service(db_session: Session):
    return CommentService(db_session)


@pytest.fixture
def post(db_session: Session):
    new_post = Post(title="Test Post", content="This is a test post", owner_id=1)
    db_session.add(new_post)
    db_session.commit()
    return new_post


def test_create_comment(comment_service: CommentService, post: Post):
    comment_data = CommentCreate(content="This is a test comment")
    owner_id = 1

    new_comment = comment_service.create_comment(comment_data, post.id, owner_id)

    assert new_comment.content == comment_data.content
    assert new_comment.post_id == post.id
    assert new_comment.owner_id == owner_id


def test_create_comment_with_toxic_content(comment_service: CommentService, post: Post):
    comment_data = CommentCreate(content="Toxic content example")

    with pytest.raises(HTTPException) as exc_info:
        comment_service.create_comment(comment_data, post.id, owner_id=1)
    assert exc_info.value.status_code == 400
    assert str(exc_info.value.detail) == "Comment contains toxic content and cannot be posted."


def test_get_comment_by_id(comment_service: CommentService, post: Post):
    comment_data = CommentCreate(content="Test comment")
    owner_id = 1
    comment = comment_service.create_comment(comment_data, post.id, owner_id)

    fetched_comment = comment_service.get_comment_by_id(comment.id)
    assert fetched_comment is not None
    assert fetched_comment.id == comment.id


def test_get_comments_by_post_id(comment_service: CommentService, post: Post):
    comment_data_1 = CommentCreate(content="First comment")
    comment_data_2 = CommentCreate(content="Second comment")
    comment_service.create_comment(comment_data_1, post.id, owner_id=1)
    comment_service.create_comment(comment_data_2, post.id, owner_id=1)

    comments = comment_service.get_comments_by_post_id(post.id)
    assert len(comments) == 2


def test_update_comment(comment_service: CommentService, post: Post):
    comment_data = CommentCreate(content="Original comment")
    owner_id = 1
    comment = comment_service.create_comment(comment_data, post.id, owner_id)

    update_data = CommentUpdate(content="Updated comment")
    updated_comment = comment_service.update_comment_crud(comment.id, update_data)

    assert updated_comment.content == "Updated comment"


def test_delete_comment(comment_service: CommentService, post: Post):
    comment_data = CommentCreate(content="Test comment to delete")
    owner_id = 1
    comment = comment_service.create_comment(comment_data, post.id, owner_id)

    comment_service.delete_comment_crud(comment.id)

    with pytest.raises(HTTPException):
        comment_service.get_comment_by_id(comment.id)


def test_get_comments_daily_breakdown(comment_service: CommentService, post: Post):
    comment_data = CommentCreate(content="Test comment")
    owner_id = 1

    comment_service.create_comment(comment_data, post.id, owner_id)

    breakdown = comment_service.get_comments_daily_breakdown(date_from="2023-01-01", date_to="2023-01-31")
    assert isinstance(breakdown, list)
