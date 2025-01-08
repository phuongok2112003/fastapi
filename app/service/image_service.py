import cloudinary
import cloudinary.uploader
from fastapi import  UploadFile
from fastapi_sqlalchemy import db
from typing import List
from app.schemas.sche_image import ImageResponse,ImageBase,ImageRequest
from app.model.models import Image
from fastapi.security import HTTPBearer
from app.until.exception_handler import CustomException
from app.service.user_service import UserService
# Cấu hình Cloudinary
cloudinary.config(
    cloud_name="phuongxuan",
    api_key="669542331435496",
    api_secret="xvFYRVXvX-7N5Cd-7xRNjWFE6i4",
)

class ImageService:
    def __init__(self):
        self.db=db.session
        self.user_service=UserService()

    async def upload_image(self,files : List[UploadFile],auth2:HTTPBearer)->ImageResponse:
        file_urls = ImageResponse(imgase=[])
        user= self.user_service.get_current_user(auth2)
        if not user:
            raise CustomException(http_code=401, code="401", message="Chưa đăng nhập hoặc không có quyền")
        for file in files:
                
                file_content = await file.read()
                
                upload_result = cloudinary.uploader.upload(file_content, folder="uploads/")
                image = ImageBase(url=upload_result["url"], public_id=upload_result["public_id"])
                file_urls.imgase.append(image)
            
            
        return file_urls
    async def delete_image(self,images : ImageRequest,auth2:HTTPBearer):
        
        user= self.user_service.get_current_user(auth2)
        if not user:
            raise CustomException(http_code=401, code="401", message="Chưa đăng nhập hoặc không có quyền")
        for image in images.imgase:
            try:
            # Xóa ảnh từ Cloudinary bằng public_id
                cloudinary.uploader.destroy(image.public_id)
              
            except Exception as e:
                return {"error": str(e)}
        return {"message": "Image with public_id  has been deleted successfully."}



