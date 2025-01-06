from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.sche_user import UserCreate, UserResponse, EmailPass
from app.schemas.sche_base import DataResponse
from app.schemas.sche_token import Token
from app.service.user_service import UserService
from app.db.session import get_db
from app.core.security import create_access_token
from typing import Any
from app.core.config import auth
from fastapi.security import HTTPBearer
from app.schemas.sche_page import PaginationParams
from app.until.page import Page
router = APIRouter()

@router.post("/login", response_model=DataResponse[Token])
def logins(user: EmailPass, user_service: UserService= Depends()):
    user_login = user_service.login(email_password=user)
    if not user_login:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    
    # Tạo token
    token = Token(access_token=create_access_token(user_login))
    
    # Trả về DataResponse với Token
    return DataResponse().success_response(data=token)


@router.get("/me", response_model=DataResponse[UserResponse])
def detail_me(user_service: UserService= Depends(),auth2:HTTPBearer =Depends(auth)):
    """
    API get detail current User
    """
    current_user = user_service.get_current_user(http_authorization_credentials=auth2)
    return DataResponse().success_response(data=UserResponse(**current_user.__dict__))

@router.get("/page/", response_model=DataResponse[Page[UserResponse]])
async def read(param:PaginationParams=Depends(), user_service: UserService= Depends() ):
    return DataResponse().success_response(data=user_service.get_page_user(param=param))

@router.post("/", response_model=UserResponse)
def create(user: UserCreate, user_service: UserService= Depends() ):
    return user_service.create_user(user)


@router.get("/{user_id}", response_model=UserResponse)
async def read(user_id: int, user_service: UserService= Depends() ):
    return user_service.get_user(user_id)


