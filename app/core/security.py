import jwt
from typing import Union , Any
from datetime import datetime,timedelta
from app.core.config import settings
from app.model.models import User
from passlib.context import CryptContext

pwd_context=CryptContext(schemes=['bcrypt'],deprecated="auto")

def create_access_token(user : Union[User,Any])->str:
    exprie=datetime.utcnow()+timedelta(
        seconds=settings.ACCESS_TOKEN_EXPIRE_SECONDS
    )
    to_encode={
        'exp':exprie,
        'user_id': user.id,
        'email': user.email
    }
    
    return jwt.encode(to_encode,settings.SECRET_KEY,algorithm=settings.SECURITY_ALGORITHM)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)