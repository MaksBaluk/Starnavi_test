from typing import Optional
from fastapi import Form
from pydantic import BaseModel, EmailStr, Field

from .models import User
from src.posts.schemas import Post
from src.comments.schemas import Comment


# Token Schemas----------------------------------------------------
class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


class TokenData(BaseModel):
    email: EmailStr | None = None


# User Schemas----------------------------------------------------
class UserBase(BaseModel):
    email: EmailStr
    username: str = Field(..., max_length=50)

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True


class User(UserBase):
    id: int

    posts: Optional[list[Post]] = []
    comments: Optional[list[Comment]] = []

    # @classmethod
    # def from_orm(cls, user: User):
    #     posts = user.posts
    #     comments = user.comments
    #     return cls(id=user.id, username=user.username, posts=posts, comments=comments)

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True


class UserCreate(UserBase):
    password: str

    class Config:
        from_attributes = True


class Login(BaseModel):
    email: EmailStr


class UserProfile(BaseModel):
    username: str

    posts: list[Post] = []

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True
