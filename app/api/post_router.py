from fastapi import APIRouter, Depends
from app.schemas.sche_post import PostCreate, PostResponse
from app.service.post_service import PostService
from app.until.authen_login import login_required
from app.model.models import User
from app.schemas.sche_page import PaginationParams
from app.until.page import Page
from app.schemas.sche_base import DataResponse
router = APIRouter()




@router.post("/", response_model=DataResponse[object])
def create(post: PostCreate,postservice:PostService=Depends(),user:User=Depends(login_required)):
    return DataResponse().success_response(data=postservice.create_post(post,user= user))


@router.get("/", response_model=DataResponse[Page[PostResponse]])
def read(param:PaginationParams=Depends(),postservice:PostService=Depends()):
    return DataResponse().success_response(data=postservice.get_posts(param=param))
