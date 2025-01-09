from app.model.models import Comment,User,Friend,Post,Favorite,Image
from app.schemas.sche_comment import CommentResponse
from app.schemas.sche_user import UserResponse
from app.schemas.sche_friend import FriendResponse
from app.schemas.sche_post import PostResponse
from app.schemas.sche_favorites import FavoriteResponde
from app.schemas.sche_image import ImageResponse,ImageBase
from typing import List

def comment_mapper(comment:Comment)->CommentResponse:
     return CommentResponse(id=comment.id,username=comment.author.name,post_id=comment.post_id,createdAt=comment.updated_at.isoformat(),content=comment.content)
def user_mapper(user:User)->UserResponse:
     return UserResponse(**user.__dict__)
def friend_mapper(friend:Friend)->FriendResponse:
     return FriendResponse(id=friend.id,createdAt=friend.created_at.isoformat(),receiver=user_mapper(friend.receiver),sender=user_mapper(friend.sender),statuts=friend.status)
def favorite_mapper(favoirte:Favorite)->FavoriteResponde:
     return FavoriteResponde(createdAt=favoirte.updated_at.isoformat(),id=favoirte.id,post_id=favoirte.post_id,username=favoirte.author.name)
def image_mapper(image:List[Image])->ImageResponse:
     list_anh=[]
     for anh in image:
          anh_response=ImageBase(url=anh.url)
          list_anh.append(anh_response)
     return ImageResponse(imgase=list_anh)
def post_mapper(post:Post)->PostResponse:
     return PostResponse(content=post.content,user=user_mapper(post.author),
                         comment= [  comment_mapper(comment)for comment in post.comments ],
                         favorite=[favorite_mapper(lik) for lik in post.favorites],
                         id=post.id,
                         title=post.title,
                         image_response=image_mapper(post.images)
                         
                         )