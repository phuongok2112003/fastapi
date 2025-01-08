from fastapi import APIRouter, Depends
from app.schemas.sche_post import PostCreate, PostResponse
from app.service.post_service import PostService
from app.core.config import auth
from fastapi.security import HTTPBearer
router = APIRouter()




@router.post("/", response_model=PostResponse)
def create(post: PostCreate,postservice:PostService=Depends(),auth2:HTTPBearer=Depends(auth)):
    return postservice.create_post(post,auth2=auth2)


@router.get("/", response_model=list[PostResponse])
def read(skip: int = 0, limit: int = 10,postservice:PostService=Depends()):
    return postservice.get_posts(skip=skip,limit=limit)
