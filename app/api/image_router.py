import cloudinary
import cloudinary.uploader
from fastapi import APIRouter, File, UploadFile,Depends
from app.schemas.sche_base import DataResponse
from app.schemas.sche_image import ImageResponse,ImageRequest
from app.core.config import auth
from fastapi.security import HTTPBearer
from app.service.image_service import ImageService
from typing import List 
router = APIRouter()
# Cấu hình Cloudinary
cloudinary.config(
    cloud_name="dr5vp5cga",
    api_key="669542331435496",
    api_secret="xvFYRVXvX-7N5Cd-7xRNjWFE6i4",
)


@router.post("/upload/", response_model=DataResponse[ImageResponse])
async def upload_to_cloudinary(files: List[UploadFile] = File(...),image_service:ImageService=Depends(),auth2:HTTPBearer=Depends(auth)):
    result = await image_service.upload_image(files=files, auth2=auth2)
    
    # Trả về response với DataResponse
    return DataResponse().success_response(data=result)


@router.delete("/delete/", response_model=DataResponse[object])
async def upload_to_cloudinary(images : ImageRequest,image_service:ImageService=Depends(),auth2:HTTPBearer=Depends(auth)):
    result = await image_service.delete_image(images=images, auth2=auth2)
    
    # Trả về response với DataResponse
    return DataResponse().success_response(data=result)
