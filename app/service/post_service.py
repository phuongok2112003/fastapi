from app.model.models import Post,Image
from app.schemas.sche_post import PostCreate
from fastapi_sqlalchemy import db
from app.model.models import User
from app.service.image_service import ImageService
import requests
from app.until.exception_handler import CustomException
from app.until.get_public_id import extract_public_id
from app.service.mapper.Mapper import post_mapper
from app.until.page import paginate,Page
from app.schemas.sche_page import PaginationParams
from app.schemas.sche_post import PostResponse
class PostService:
    def __init__(self):
        self.db=db.session
        self.image_service=ImageService()
    
    def check_image_exists(self,url:str):
        response = requests.head(url)
        return response.status_code == 200
    
    def create_post(self, post: PostCreate, user: User):
        # Tạo đối tượng Post
        db_post = Post(title=post.title, content=post.content, author_id=user.id)
        
        # Thêm post vào database trước
        self.db.add(db_post)
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



    def get_posts(self,param:PaginationParams)->"Page[PostResponse]":
        _query=self.db.query(Post)
        return paginate(model=Post,model_response=post_mapper ,query=_query,params=param)
