from pydantic import BaseModel
from typing import Optional
class CommentBase(BaseModel):
    content: str
    class Config:
        from_attributes=True

class CommentRequest(CommentBase):
    pass 
class CommentResponse(CommentBase):
    id:int
    username: str
    post_id : int
    createdAt : str