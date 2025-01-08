from fastapi import APIRouter, Depends
from app.service.favorite_service import FavoriteService
from app.schemas.sche_base import DataResponse
from app.core.config import auth
from fastapi.security import HTTPBearer

router = APIRouter()

@router.post("/add_like", response_model=DataResponse[object])
def create(post_id:int,favorite_service:FavoriteService=Depends(),auth2:HTTPBearer=Depends(auth)):
    return  DataResponse().success_response(data=favorite_service.like(post_id=post_id,auth2=auth2))

@router.delete("/un_like", response_model=DataResponse[object])
def update(post_id:int,favorite_service:FavoriteService=Depends(),auth2:HTTPBearer=Depends(auth)):
    return  DataResponse().success_response(data=favorite_service.un_like(post_id=post_id,auth2=auth2))

