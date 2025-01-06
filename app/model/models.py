from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.model.model_base import BareBaseModel


class User(BareBaseModel):
    
    name = Column(String(100), nullable=False)
    age = Column(Integer, nullable=True)
    role = Column(String(50), nullable=False, default="user")
    email = Column(String(100), nullable=False, unique=True)
    password = Column(String(200), nullable=False) 
    posts = relationship("Post", back_populates="author")


class Post(BareBaseModel):
   
    title = Column(String(200), nullable=False)
    content = Column(Text, nullable=False)
    author_id = Column(Integer, ForeignKey("user.id"))

    author = relationship("User", back_populates="posts")
