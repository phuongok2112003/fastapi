from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.sche_post import PostCreate, PostResponse
from app.service.post_service import create_post, get_posts
from app.db.session import get_db

router = APIRouter()




@router.post("/", response_model=PostResponse)
def create(post: PostCreate, db: Session = Depends(get_db)):
    return create_post(db, post)


@router.get("/", response_model=list[PostResponse])
def read(db: Session = Depends(get_db)):
    return get_posts(db)
