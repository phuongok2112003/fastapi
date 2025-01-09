from pydantic import BaseModel
from typing import Optional,List
from app.schemas.sche_image import ImageRequest,ImageResponse
from app.schemas.sche_comment import CommentResponse
from app.schemas.sche_favorites import FavoriteResponde
from app.schemas.sche_user import UserResponse

class PostBase(BaseModel):
    title: str
    content: str


class PostCreate(PostBase):
    image_request: Optional[ImageRequest]=None
    
class PostResponse(PostBase):
    id: int
    image_response:Optional[ImageResponse] = None
    user:UserResponse
    favorite:List[FavoriteResponde]
    comment:List[CommentResponse]


    class Config:
        from_attributes=True
