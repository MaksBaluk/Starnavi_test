from datetime import datetime

from pydantic import BaseModel, Field
from src.comments.schemas import Comment


# Post Schemas ---------------------------------------------------------------
class PostBase(BaseModel):
    title: str = Field(..., max_length=100)
    content: str

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True


class Post(PostBase):
    id: int
    created_at: datetime
    updated_at: datetime
    owner_id: int

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True


class PostOne(Post):
    comments: list[Comment] = Field(default_factory=list)

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True


class PostCreate(PostBase):
    class Config:
        from_attributes = True
        arbitrary_types_allowed = True


class PostUpdate(PostBase):
    title: str | None = None
    content: str | None = None

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True
