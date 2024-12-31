from sqlalchemy.orm import Session
from app.model.models import User
from app.schemas.sche_token import TokenPayload
from fastapi.security import HTTPBearer
from app.schemas.sche_user import UserCreate,EmailPass
from app.core.security import verify_password,get_password_hash
from typing import Optional
from fastapi import Depends, HTTPException
from pydantic import ValidationError
from app.core.config import settings
import jwt
from starlette import status
reusable_oauth2 = HTTPBearer(
    scheme_name='Authorization'
)
def create_user(db: Session, user: UserCreate):
    exist_user = db.query(User).filter(User.email == user.email).first()
    if exist_user:
        raise Exception('Email already exists')
    db_user = User(name=user.name, age=user.age, role=user.role,email=user.email,password=get_password_hash(user.password))
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_current_user(db:Session,http_authorization_credentials:HTTPBearer) -> User:
 
        try:
            payload = jwt.decode(
                http_authorization_credentials.credentials, settings.SECRET_KEY,
                algorithms=[settings.SECURITY_ALGORITHM]
            )
            token_data = TokenPayload(**payload)
        except (jwt.PyJWTError, ValidationError):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Could not validate credentials",
            )
        user = db.query(User).get(token_data.user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user

def check_role(role:tuple,db:Session,http_authorization_credentials:HTTPBearer):
    user=get_current_user(db,http_authorization_credentials)
    if user.role not in role and role:
          raise HTTPException(status_code=400,
                                detail=f'User {user.email} can not access this api')
    

def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def get_users(db: Session, skip: int = 0, limit: int = 10):
    return db.query(User).offset(skip).limit(limit).all()

def login(db:Session,email_password:EmailPass)-> Optional[User]:
    user=db.query(User).filter(User.email==email_password.email).first()
    if not user:
        return None
    if not verify_password(email_password.password,user.password):
        return None
    return user