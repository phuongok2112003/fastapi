from app.model.models import Post,Comment
from fastapi_sqlalchemy import db
from app.service.user_service import UserService
from app.schemas.sche_comment import CommentRequest, CommentResponse
from fastapi.security import HTTPBearer
from app.until.exception_handler import CustomException
from app.schemas.sche_page import PaginationParams
from app.until.page import paginate,Page
from app.service.mapper.Mapper import comment_mapper
class CommentService:
    def __init__(self):
        self.db=db.session
        self.user_service=UserService()
      
    def add_comment(self,post_id:int,comment_request:CommentRequest,auth2:HTTPBearer)->CommentResponse:
        user= self.user_service.get_current_user(auth2)
        if not user:
            raise CustomException(http_code=401, code="401", message="Chưa đăng nhập hoặc không có quyền")
        post=self.db.query(Post).filter(Post.id==post_id).first()
        if post is None:
            raise CustomException(http_code=400,code="400",message="post id khong ton tai")
        
        else :
            comment = Comment()
            comment.content=comment_request.content
            comment.author_id=user.id
            comment.post_id=post.id
            self.db.add(comment)
            self.db.commit()
            self.db.refresh(comment)
            return comment_mapper(comment=comment)
    def update_commmet(self,comment_id:int,comment_request:CommentRequest,auth2:HTTPBearer)->CommentResponse:
        comment=self.db.query(Comment).filter(Comment.id==comment_id).first()
        user= self.user_service.get_current_user(auth2)
        if not user:
            raise CustomException(http_code=401, code="401", message="Chưa đăng nhập hoặc không có quyền")
        if comment.author_id !=user.id:
             raise CustomException(http_code=403,code="403",message="Ban khong co quyen")
        if comment is None:
            raise CustomException(http_code=400,code="400",message="Comment id khong ton tai")
        comment.content=comment_request.content
        self.db.add(comment)
        self.db.commit()
        self.db.refresh(comment)
        return comment_mapper(comment=comment)
    def delete_comment(self,comment_id:int,auth2:HTTPBearer):
        comment=self.db.query(Comment).filter(Comment.id==comment_id).first()
        user= self.user_service.get_current_user(auth2)
        if not user:
            raise CustomException(http_code=401, code="401", message="Chưa đăng nhập hoặc không có quyền")
        if comment is None:
            raise CustomException(http_code=400,code="400",message="Comment id khong ton tai")
        if comment.author_id !=user.id:
                raise CustomException(http_code=403,code="403",message="Ban khong co quyen")   
        # if not self.db.is_modified(comment):
        #     self.db.add(comment)

        self.db.refresh(comment)
        self.db.delete(comment)
        self.db.commit()
      
        return {"message": "Bình luận đã được xóa thành công"}
    def get_page(self,post_id:int,param:PaginationParams)->"Page[CommentResponse]":
        _query=self.db.query(Comment).filter(Comment.post_id==post_id)
        return paginate(model=Comment,model_response=comment_mapper,query=_query,params=param)

