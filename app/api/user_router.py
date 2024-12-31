from fastapi import APIRouter, Depends,HTTPException
from sqlalchemy.orm import Session
from app.schemas.sche_user import UserCreate, UserResponse,EmailPass
from app.schemas.sche_base import DataResponse
from app.schemas.sche_token import Token
from app.service.user_service import create_user, get_user, get_users,login,get_current_user,reusable_oauth2
from app.db.session import get_db
from app.core.security import create_access_token
from typing import Any
router = APIRouter()

@router.post("/login",  response_model=DataResponse[Token])
def logins(user: EmailPass, db: Session = Depends(get_db)):
    user_login =login(db=db,email_password=user)
    if not user_login:
        raise HTTPException(status_code=400, detail='Incorrect email or password')
    return DataResponse().success_response(
        {
            'access_token': create_access_token(user_login)

        }
    )
@router.get("/me", response_model=DataResponse[UserResponse])
def detail_me( db: Session = Depends(get_db),http_authorization_credentials=Depends(reusable_oauth2)) -> Any:
    """
    API get detail current User
    """
    current_user= get_current_user(db=db,http_authorization_credentials=http_authorization_credentials)
    return DataResponse().success_response(data=UserResponse(**current_user.__dict__))

@router.post("/", response_model=UserResponse)
def create(user: UserCreate, db: Session = Depends(get_db)):
    return create_user(db, user)

@router.get("/{user_id}", response_model=UserResponse)
async def read(user_id: int, db: Session = Depends(get_db)):
    return get_user(db, user_id)


