from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.sche_user import UserCreate, UserResponse, EmailPass
from app.schemas.sche_base import DataResponse
from app.schemas.sche_token import Token
from app.service.user_service import UserService
from app.db.session import get_db
from app.core.security import create_access_token
from typing import Any

router = APIRouter()

# Dependency Injection để cung cấp UserService



@router.post("/login", response_model=DataResponse[Token])
def logins(user: EmailPass, user_service: UserService ):
    user_login = user_service.login(email_password=user)
    if not user_login:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    return DataResponse().success_response({
        'access_token': create_access_token(user_login)
    })


@router.get("/me", response_model=DataResponse[UserResponse])
def detail_me(user_service: UserService ,http_authorization_credentials=Depends(UserService.reusable_oauth2)):
    """
    API get detail current User
    """
    current_user = user_service.get_current_user(http_authorization_credentials.credentials)
    return DataResponse().success_response(data=UserResponse(**current_user.__dict__))


@router.post("/", response_model=UserResponse)
def create(user: UserCreate, user_service: UserService ):
    return user_service.create_user(user)


@router.get("/{user_id}", response_model=UserResponse)
async def read(user_id: int, user_service: UserService ):
    return user_service.get_user(user_id)
