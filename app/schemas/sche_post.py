from pydantic import BaseModel
from typing import Optional


class PostBase(BaseModel):
    title: str
    content: str


class PostCreate(PostBase):
    pass


class PostResponse(PostBase):
    id: int

    class Config:
        from_attributes=True
