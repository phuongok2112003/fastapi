from pydantic import BaseModel,EmailStr
from typing import List, Optional


class UserBase(BaseModel):
    name: str
    age: Optional[int]
    role: str
    email: EmailStr
  
    class Config:
        from_attributes=True


class UserCreate(UserBase):
    password: str
    

class EmailPass(BaseModel):
    email: EmailStr
    password: str


class UserResponse(UserBase):
    id: int
    posts: List[dict] = []

  
