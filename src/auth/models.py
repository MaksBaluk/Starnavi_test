from sqlalchemy.orm import Mapped, mapped_column, relationship, deferred
from sqlalchemy import String
from src.core.base import Base, created_time, updated_time


class User(Base):
    __tablename__ = 'users'

    email: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    username: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[created_time]
    updated_at: Mapped[updated_time]

    posts: Mapped[list["Post"]] = deferred(relationship('Post', back_populates='owner', cascade="all, delete-orphan"))
    comments: Mapped[list["Comment"]] = deferred(relationship('Comment', back_populates='owner', cascade="all, delete-orphan"))


