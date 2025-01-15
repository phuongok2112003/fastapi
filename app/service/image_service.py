import cloudinary
import cloudinary.uploader
from fastapi import  UploadFile
from fastapi_sqlalchemy import db
from typing import List
from app.schemas.sche_image import ImageResponse,ImageBase,ImageRequest
from app.model.models import Image
from app.until.exception_handler import CustomException
from app.core.config import settings
from app.until.get_public_id import extract_public_id
from starlette import status
cloudinary.config(
    cloud_name=settings.CLOUD_NAME,
    api_key=settings.API_KEY,
    api_secret=settings.API_SECRET,
)

class ImageService:
    def __init__(self):
        self.db=db.session
        

    async def upload_image(self,files : List[UploadFile])->ImageResponse:
        file_urls = ImageResponse(imgase=[])
       
        for file in files:
                
                file_content = await file.read()
                
                upload_result = cloudinary.uploader.upload(file_content, folder="uploads/")
                image = ImageBase(url=upload_result["url"], public_id=upload_result["public_id"])
                file_urls.imgase.append(image)
            
            
        return file_urls
    async def delete_image(self,images : ImageRequest):
        
      
        for image in images.imgase:
            try:
            # Xóa ảnh từ Cloudinary bằng public_id
                cloudinary.uploader.destroy(extract_public_id(image.url))
              
            except Exception as e:
                raise CustomException(http_code=status.HTTP_400_BAD_REQUEST,code="400",message=e)
               
        return {"message": "Image with public_id  has been deleted successfully."}



