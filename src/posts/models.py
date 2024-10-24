from sqlalchemy.orm import Mapped, mapped_column, relationship, deferred
from sqlalchemy import String, Text, ForeignKey, Boolean
from src.core.base import Base, created_time, updated_time


class Post(Base):
    __tablename__ = 'posts'

    title: Mapped[str] = mapped_column(String(100), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    owner_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'), index=True, nullable=False)
    created_at: Mapped[created_time]
    updated_at: Mapped[updated_time]
    auto_reply_enabled: Mapped[bool] = mapped_column(Boolean, default=False)

    owner: Mapped["User"] = relationship("User", back_populates="posts")
    comments: Mapped[list["Comment"]] = relationship("Comment", back_populates="post", cascade="all, delete-orphan")



