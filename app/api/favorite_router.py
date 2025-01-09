from fastapi import APIRouter, Depends
from app.service.favorite_service import FavoriteService
from app.schemas.sche_base import DataResponse
from app.core.config import auth
from fastapi.security import HTTPBearer
from app.until.authen_login import login_required
from app.model.models import User
router = APIRouter()

@router.post("/add_like", response_model=DataResponse[object])
def create(post_id:int,favorite_service:FavoriteService=Depends(),user:User=Depends(login_required)):
    return  DataResponse().success_response(data=favorite_service.like(post_id=post_id,user= user))

@router.delete("/un_like", response_model=DataResponse[object])
def update(post_id:int,favorite_service:FavoriteService=Depends(),user:User=Depends(login_required)):
    return  DataResponse().success_response(data=favorite_service.un_like(post_id=post_id,user= user))

