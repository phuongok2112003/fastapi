from pydantic import BaseModel
from typing import Optional
from app.until.enums import FriendshipStatus
from app.schemas.sche_user import UserResponse
class FriendBase(BaseModel):
   
    statuts: FriendshipStatus
    class Config:
        from_attributes=True
class FriendRequest(FriendBase):
    pass 
class FriendResponse(FriendBase):
    id:int
    sender : UserResponse
    receiver : UserResponse
    createdAt : str