from pydantic import BaseModel
from typing import Optional


class PostBase(BaseModel):
    title: str
    content: str


class PostCreate(PostBase):
    author_id: int


class PostResponse(PostBase):
    id: int

    class Config:
        from_attributes=True
