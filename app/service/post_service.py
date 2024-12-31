from sqlalchemy.orm import Session
from app.model.models import Post
from app.schemas.sche_post import PostCreate


def create_post(db: Session, post: PostCreate):
    db_post = Post(title=post.title, content=post.content, author_id=post.author_id)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post


def get_posts(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Post).offset(skip).limit(limit).all()
