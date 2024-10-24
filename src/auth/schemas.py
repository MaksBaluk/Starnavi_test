from typing import Optional
from fastapi import Form
from pydantic import BaseModel, EmailStr, Field
from fastapi.security import OAuth2PasswordRequestForm


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


class User(UserBase):
    id: int
    role_id: Optional[int]
    is_active: bool
    is_superuser: bool
    is_verified: bool

    # posts: list[Post] = []
    # comments: list[Comment] = []

    class Config:
        from_attributes = True


class UserCreate(UserBase):
    password: str

    class Config:
        from_attributes = True


class Login(BaseModel, OAuth2PasswordRequestForm):
    email: EmailStr


class UserProfile(BaseModel):
    username: str

    # posts: list[Post] = []

    class Config:
        from_attributes = True


class Username(BaseModel):
    username: str

    class Config:
        from_attributes = True
