from pydantic import BaseModel
from typing import List ,Optional # Import List từ typing

class ImageBase(BaseModel):
    url: Optional[str]=None
    

    class Config:
        from_attributes = True

class ImageRequest(BaseModel):  # Kế thừa từ BaseModel
    imgase: Optional[List[ImageBase]]=None  # Sử dụng List từ typing để khai báo danh sách

    class Config:
        from_attributes = True

class ImageResponse(BaseModel):  # Kế thừa từ BaseModel
    imgase: List[ImageBase]  # Sử dụng List từ typing để khai báo danh sách

    class Config:
        from_attributes = True
