from sqlalchemy import Column, Integer, String, Text, ForeignKey,Enum as SQLAlchemyEnum
from sqlalchemy.orm import relationship
from app.model.model_base import BareBaseModel
from app.until.enums import FriendshipStatus

class User(BareBaseModel):
    
    name = Column(String(100), nullable=False)
    age = Column(Integer, nullable=True)
    role = Column(String(50), nullable=False, default="user")
    email = Column(String(100), nullable=False, unique=True)
    password = Column(String(200), nullable=False) 

    posts = relationship("Post", back_populates="author")
    comments = relationship("Comment",back_populates="author")
    favorites =relationship("Favorite",back_populates="author")
    images =relationship("Image",back_populates="author")
    sent_friend_requests = relationship("Friend", foreign_keys="Friend.sender_id", back_populates="sender", cascade="all, delete-orphan")
    received_requests = relationship("Friend", foreign_keys="Friend.receiver_id", back_populates="receiver", cascade="all, delete-orphan")
class Post(BareBaseModel):
   
    title = Column(String(200), nullable=False)
    content = Column(Text, nullable=False)
    author_id = Column(Integer, ForeignKey("user.id"))

    author = relationship("User", back_populates="posts")
    comments = relationship("Comment",back_populates="posts")
    images=relationship("Image",back_populates="posts")
    favorites=relationship("Favorite",back_populates="posts")
class Comment(BareBaseModel):
    content =Column(Text, nullable=False)
    author_id = Column(Integer, ForeignKey("user.id"))
    post_id=Column(Integer,ForeignKey("post.id"))

    author = relationship("User", back_populates="comments")
    posts =relationship("Post",back_populates="comments")
class Favorite(BareBaseModel):
    author_id = Column(Integer, ForeignKey("user.id"))
    post_id=Column(Integer,ForeignKey("post.id"))
     
    posts =relationship("Post",back_populates="favorites") 
    author = relationship("User", back_populates="favorites")
    


class Image(BareBaseModel):
    url=Column(String(200),nullable=False)
    post_id=Column(Integer,ForeignKey("post.id"))
    author_id=Column(Integer,ForeignKey("user.id"))
    public_id=Column(str(200),primary_key=True)
    
    author = relationship("User", back_populates="images")
    posts =relationship("Post",back_populates="images")

class Friend(BareBaseModel):
    sender_id= Column(Integer,ForeignKey("user.id"),nullable=False)
    receiver_id= Column(Integer,ForeignKey('user.id'),nullable=False)
    status = Column(SQLAlchemyEnum(FriendshipStatus), default=FriendshipStatus.PENDING)

    sender = relationship("User", foreign_keys=[sender_id], back_populates="sent_friend_requests")
    receiver = relationship("User", foreign_keys=[receiver_id], back_populates="received_requests")
