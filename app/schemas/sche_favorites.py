from pydantic import BaseModel
from typing import Optional

class FavoriteResponde(BaseModel):
    id:int
    username:str
    post_id:int
    createdAt:str
    class Config:
        from_attributes=True