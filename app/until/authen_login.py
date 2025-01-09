from fastapi import Depends
from fastapi.security import HTTPBearer
from app.service.user_service import UserService
from app.core.config import auth

def login_required(http_authorization_credentials:HTTPBearer=Depends(auth)):
    return UserService().get_current_user(http_authorization_credentials)