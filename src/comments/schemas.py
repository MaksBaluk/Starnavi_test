from datetime import datetime

from pydantic import BaseModel


# Comment Schemas ---------------------------------------------------------------

class CommentBase(BaseModel):
    content: str


class Comment(CommentBase):
    id: int
    created_at: datetime
    updated_at: datetime
    owner_id: int
    post_id: int

    class Config:
        from_attributes = True


class CommentCreate(CommentBase):
    class Config:
        from_attributes = True


class CommentUpdate(CommentBase):
    content: str | None = None
