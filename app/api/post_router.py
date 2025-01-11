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
def read(user:User=Depends(login_required),param:PaginationParams=Depends(),postservice:PostService=Depends()):
    return DataResponse().success_response(data=postservice.get_posts(param=param,user=user))

@router.patch("/{post_id}", response_model=DataResponse[Page[PostResponse]])
def read(post_id:int,post: PostCreate,user:User=Depends(login_required),postservice:PostService=Depends()):
    return DataResponse().success_response(data=postservice.update_post(post_id=post_id,post=post,user=user))

@router.get("/{post_id}", response_model=DataResponse[PostResponse],dependencies=[Depends(login_required)])
def read(post_id:int,postservice:PostService=Depends()):
    return DataResponse().success_response(data=postservice.get_post_by_id(post_id=post_id))

@router.delete("/{post_id}", response_model=DataResponse[object])
async def read(post_id:int,user:User=Depends(login_required),postservice:PostService=Depends()):
    return DataResponse().success_response(data= await postservice.delete_post(post_id=post_id,user=user))
