from fastapi import APIRouter, Depends
from app.schemas.sche_friend import FriendResponse
from app.service.friend_service import FriendService
from app.until.page import Page
from app.schemas.sche_base import DataResponse
from app.core.config import auth
from fastapi.security import HTTPBearer
from app.schemas.sche_page import PaginationParams
from app.until.enums import FriendshipStatus
from app.schemas.sche_user import UserResponse
from app.until.authen_login import login_required
from app.model.models import User
router = APIRouter()

@router.post("/add-friend", response_model=DataResponse[FriendResponse])
def add_friend(receiver_id:int,friend_service:FriendService=Depends(),user:User=Depends(login_required)):
    return  DataResponse().success_response(data=friend_service.add_friend(receiver_id=receiver_id,sender= user))

@router.post("/response-friend", response_model=DataResponse[FriendResponse])
def response_friend(sender_id:int,request_friend:FriendshipStatus,friend_service:FriendService=Depends(),user:User=Depends(login_required)):
    return  DataResponse().success_response(data=friend_service.response_friend(sender_id=sender_id,request=request_friend,user= user))


@router.get("/list-friend", response_model=DataResponse[Page[UserResponse]])
def response_friend(param:PaginationParams=Depends(),friend_service:FriendService=Depends(),user:User=Depends(login_required)):
    return  DataResponse().success_response(data=friend_service.get_list_friend(param=param,user= user))

@router.get("/list-friend-reciver", response_model=DataResponse[Page[FriendResponse]])
def response_friend(param:PaginationParams=Depends(),friend_service:FriendService=Depends(),user:User=Depends(login_required)):
    return  DataResponse().success_response(data=friend_service.get_list_pending(param=param,user= user))
