from typing import Type
from .models import User
from .schemas import UserCreate
from core.base import BaseService
from .utils import get_password_hash


class UserService(BaseService):
    """User CRUD actions class"""

    def create_user(self, data: UserCreate) -> User:
        user = User(email=data.email,
                    password=get_password_hash(data.password),
                    username=data.username)
        self.create(user)
        return user

    def get_user_by_id(self, user_id: int) -> Type[User] | None:
        return self.db.query(User).filter(User.id == user_id).first()

    def get_user_by_email(self, email: str) -> Type[User] | None:
        return self.db.query(User).filter(User.email == email).first()

    def get_user_by_username(self, username: str) -> Type[User] | None:
        return self.db.query(User).filter(User.username == username).first()

    def get_all_users_crud(self) -> list[Type[User]]:
        return self.db.query(User).all()

    def delete_user(self, user_id: int) -> None:
        user = self.get_user_by_id(user_id)
        self.delete(user)
