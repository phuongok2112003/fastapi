from app.model.models import Post,Image,User,Friend
from app.schemas.sche_post import PostCreate
from fastapi_sqlalchemy import db
from app.model.models import User
from app.service.image_service import ImageService
import requests
from app.until.exception_handler import CustomException
from app.until.get_public_id import extract_public_id
from app.service.mapper.Mapper import post_mapper,image_mapper_request
from app.until.page import paginate,Page
from app.schemas.sche_page import PaginationParams
from app.schemas.sche_post import PostResponse
from sqlalchemy import or_, and_
from app.until.enums import FriendshipStatus
class PostService:
    def __init__(self):
        self.db=db.session
        self.image_service=ImageService()
    
    def check_image_exists(self,url:str):
        try:
            response = requests.head(url, timeout=5)  # Thêm timeout để tránh chờ lâu
            if response.status_code != 200:
               return False
            return True
        except requests.exceptions.RequestException as e:
     
            raise CustomException(
                http_code=400,
                code="400",
                message=f"Không thể kiểm tra link ảnh: {url}. Lỗi: {str(e)}"
            )
    
    def create_post(self, post: PostCreate, user: User):
        list_anh = []  # Khởi tạo danh sách hình ảnh
        db_post = Post(title=post.title, content=post.content, author_id=user.id)

        if post.image_request.imgase:
            for image in post.image_request.imgase:
                if self.check_image_exists(image.url):  # Kiểm tra link ảnh tồn tại
                    anh = Image(
                        author=user,
                        posts=db_post,
                        public_id=extract_public_id(image.url),
                        url=image.url
                    )
                    list_anh.append(anh)
                else:
                    raise CustomException(
                        http_code=400,
                        code="400",
                        message=f"Link ảnh không tồn tại: {image.url}"
                    )
        
        # Thêm tất cả hình ảnh vào database
            if list_anh :
                self.db.add_all(list_anh)
                self.db.commit()

        # Thêm post vào database trước
        self.db.add(db_post)
        self.db.commit()
        self.db.refresh(db_post)  # Đảm bảo `db_post.id` được tạo
        
       
        
        # Trả về post đã được tạo
        return post_mapper(db_post)



    def get_posts(self,user:User,param:PaginationParams)->"Page[PostResponse]":
        user_id=user.id
        _query=self.db.query(Post).join(User,Post.author_id==User.id).outerjoin(Friend,
              and_(
             or_(Friend.sender_id == User.id, Friend.receiver_id == User.id), Friend.status==FriendshipStatus.ACCEPTED
           
        )).filter(
            or_(
                Friend.sender_id == user_id,
                Friend.receiver_id == user_id,
                User.id == user_id,
            )
          
        )  
   


        return paginate(model=Post,model_response=post_mapper ,query=_query,params=param)
    def update_post(self, post_id:int,post: PostCreate, user: User):
        db_post=self.db.query(Post).filter(Post.id==post_id).first()
        if not db_post:
            raise CustomException(
                        http_code=400,
                        code="400",
                        message=f"Khong tim thay bai post nao co id : {post_id}"
          
                    )
        if user.id==db_post.author_id:
             raise CustomException(
                        http_code=403,
                        code="403",
                        message="Ban khong co quyen thay doi bai viet cua nguoi khac "
                    )
        
        db_post = Post(title=post.title, content=post.content, author_id=user.id)
        
     
        self.db.commit()
        self.db.refresh(db_post)  # Đảm bảo `db_post.id` được tạo
        
        list_anh = []  # Khởi tạo danh sách hình ảnh
        
        if post.image_request.imgase:
            for image in post.image_request.imgase:
                if self.check_image_exists(image.url):  # Kiểm tra link ảnh tồn tại
                    anh = Image(
                        author=user,
                        posts=db_post,
                        public_id=extract_public_id(image.url),
                        url=image.url
                    )
                    list_anh.append(anh)
                else:
                    raise CustomException(
                        http_code=400,
                        code="400",
                        message=f"Link ảnh không tồn tại: {image.url}"
                    )
        
        # Thêm tất cả hình ảnh vào database
            if list_anh :
                self.db.add_all(list_anh)
                self.db.commit()
        
        # Trả về post đã được tạo
        return post_mapper(db_post)
    def get_post_by_id(self,post_id:int):
        db_post=self.db.query(Post).filter(Post.id==post_id).first()
        if not db_post:
            raise CustomException(
                        http_code=400,
                        code="400",
                        message=f"Khong tim thay bai post nao co id : {post_id}"
          
                    )
        return post_mapper(db_post)
    async  def delete_post(self,post_id:int,user:User):
        db_post=self.db.query(Post).filter(Post.id==post_id).first()
        if not db_post:
            raise CustomException(
                        http_code=400,
                        code="400",
                        message=f"Khong tim thay bai post nao co id : {post_id}"
          
                    )
        if user.id!=db_post.author_id:
             raise CustomException(
                        http_code=403,
                        code="403",
                        message="Ban khong co quyen thay doi bai viet cua nguoi khac ")
        image=image_mapper_request(db_post.images)
        await self.image_service.delete_image(images=image)

        for ii in db_post.images:
            self.db.delete(ii)

        self.db.delete(db_post)
        self.db.commit()
     

        return {"message": "Bai post đã được xóa thành công"}

