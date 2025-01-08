from app.schemas.sche_comment import CommentResponse
from app.model.models import Comment
from app.schemas.sche_user import UserResponse
from app.model.models import User

def comment_mapper(comment:Comment)->CommentResponse:
     return CommentResponse(id=comment.id,username=comment.author.name,post_id=comment.post_id,createdAt=comment.updated_at.isoformat(),content=comment.content)
def user_mapper(user:User)->UserResponse:
     return UserResponse(**user.__dict__)
