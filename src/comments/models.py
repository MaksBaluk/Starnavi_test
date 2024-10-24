from sqlalchemy.orm import Mapped, mapped_column, relationship, deferred
from sqlalchemy import Text, ForeignKey, Boolean
from src.core.base import Base, created_time, updated_time


class Comment(Base):
    __tablename__ = 'comments'

    content: Mapped[str] = mapped_column(Text, nullable=False)
    post_id: Mapped[int] = mapped_column(ForeignKey('posts.id', ondelete='CASCADE'), index=True, nullable=False)
    owner_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'), index=True, nullable=False)
    created_at: Mapped[created_time]
    updated_at: Mapped[updated_time]
    blocked: Mapped[bool] = mapped_column(Boolean, default=False)

    post: Mapped["Post"] = relationship("Post", back_populates="comments")
    owner: Mapped["User"] = relationship("User", back_populates="comments")
