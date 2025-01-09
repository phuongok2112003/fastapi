from fastapi import APIRouter, Depends
from app.schemas.sche_comment import CommentRequest, CommentResponse
from app.service.comment_service import CommentService
from app.until.page import Page
from app.schemas.sche_base import DataResponse
from app.core.config import auth
from fastapi.security import HTTPBearer
from app.schemas.sche_page import PaginationParams
from app.until.authen_login import login_required
from app.model.models import User
router = APIRouter()

@router.post("/", response_model=DataResponse[CommentResponse])
def create(post_id:int,comment_request:CommentRequest,comment_service:CommentService=Depends(),user:User=Depends(login_required)):
    return  DataResponse().success_response(data=comment_service.add_comment(post_id=post_id,comment_request=comment_request,user= user))

@router.put("/", response_model=DataResponse[CommentResponse])
def update(comment_id:int,comment_request:CommentRequest,comment_service:CommentService=Depends(),user:User=Depends(login_required)):
    return  DataResponse().success_response(data=comment_service.update_commmet(comment_id=comment_id,comment_request=comment_request,user= user))

@router.delete("/", response_model=DataResponse[object])
def delete(comment_id:int,comment_service:CommentService=Depends(),user:User=Depends(login_required)):
    return  DataResponse().success_response(data=comment_service.delete_comment(comment_id=comment_id,user= user))

@router.get("/get-page", response_model=DataResponse[Page[CommentResponse]])
def get_page(post_id:int,param:PaginationParams=Depends(),comment_service:CommentService=Depends()):
    return  DataResponse().success_response(data=comment_service.get_page(param=param,post_id=post_id))