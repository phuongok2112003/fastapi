from sqlalchemy.orm import Session
from app.model.models import Post
from app.schemas.sche_post import PostCreate
from fastapi_sqlalchemy import db
from app.service.user_service import UserService
from fastapi.security import HTTPBearer
class PostService:
    def __init__(self):
        self.db=db.session
        self.user_service=UserService()

    def create_post(self,post: PostCreate,auth2:HTTPBearer):
        user= self.user_service.get_current_user(auth2)
        db_post = Post(title=post.title, content=post.content, author_id=user.id)
        self.db.add(db_post)
        self.db.commit()
        self.db.refresh(db_post)
        return db_post


    def get_posts(self,skip: int = 0, limit: int = 10):
        return self.db.query(Post).offset(skip).limit(limit).all()
