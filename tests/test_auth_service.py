import pytest
from sqlalchemy.orm import Session
from src.auth.models import User
from src.auth.schemas import UserCreate
from src.auth.services import UserService
from src.auth.utils import get_password_hash


@pytest.fixture
def user_service(db_session: Session):
    return UserService(db_session)


def test_create_user(user_service: UserService):
    user_data = UserCreate(email="test@example.com", password="password123", username="testuser")
    user = user_service.create_user(user_data)

    assert user.email == user_data.email
    assert user.username == user_data.username
    assert user.password != user_data.password  


def test_get_user_by_email(user_service: UserService):
    user_data = UserCreate(email="test@example.com", password="password123", username="testuser")
    user_service.create_user(user_data)

    user = user_service.get_user_by_email("test@example.com")
    assert user is not None
    assert user.email == "test@example.com"


def test_delete_user(user_service: UserService):
    user_data = UserCreate(email="test@example.com", password="password123", username="testuser")
    user = user_service.create_user(user_data)

    user_service.delete_user(user.id)
    deleted_user = user_service.get_user_by_id(user.id)

    assert deleted_user is None
