from typing import Optional

from pydantic import BaseModel,EmailStr


class Token(BaseModel):
    access_token: str
    token_type: str = 'bearer'


class TokenPayload(BaseModel):
    user_id: Optional[int] = None
    email:EmailStr
