from fastapi import Depends
from app.model.models import User
from app.schemas.sche_token import TokenPayload
from app.schemas.sche_user import UserCreate, EmailPass,UserResponse
from app.core.security import verify_password, get_password_hash
from pydantic import ValidationError
import jwt
from fastapi.security import HTTPBearer
from app.core.config import settings
from starlette import status
from typing import Optional
from fastapi_sqlalchemy import db
from app.until.page import paginate,Page
from app.schemas.sche_page import PaginationParams
from app.service.mapper.Mapper import user_mapper
from app.until.exception_handler import CustomException
class UserService:
    def __init__(self):
        self.db = db.session
      
    def create_user(self, user: UserCreate) -> User:
        exist_user = self.db.query(User).filter(User.email == user.email).first()
        if exist_user:
            raise CustomException(http_code=status.HTTP_400_BAD_REQUEST,code="400",message="Email already exists")
           
        db_user = User(name=user.name, age=user.age, role=user.role, email=user.email, password=get_password_hash(user.password))
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def get_current_user(self,http_authorization_credentials:HTTPBearer) -> User:
        if not http_authorization_credentials:
         
            raise CustomException(http_code=401,code="401",message="Token is missing")

        try:
            payload = jwt.decode(
                http_authorization_credentials.credentials, settings.SECRET_KEY,
                algorithms=[settings.SECURITY_ALGORITHM]
            )
            token_data = TokenPayload(**payload)
        except (jwt.PyJWTError, ValidationError):
            raise CustomException(http_code=status.HTTP_403_FORBIDDEN,code="403",message="Could not validate credentials")

        user = self.db.query(User).get(token_data.user_id)
        if not user:
            raise CustomException(http_code=status.HTTP_404_NOT_FOUND,code="404",message="User not found")
          
        return user

    def get_user(self, user_id: int) -> Optional[User]:
        return self.db.query(User).filter(User.id == user_id).first()

    def get_users(self, skip: int = 0, limit: int = 10):
        return self.db.query(User).offset(skip).limit(limit).all()

    def login(self, email_password: EmailPass) -> Optional[User]:
        user = self.db.query(User).filter(User.email == email_password.email).first()
        if not user or not verify_password(email_password.password, user.password):
            return None
        return user
    
    def get_page_user(self,param:PaginationParams)->"Page[UserResponse]":
        _query=self.db.query(User)
       
        return paginate(model=User,model_response=user_mapper ,query=_query,params=param)