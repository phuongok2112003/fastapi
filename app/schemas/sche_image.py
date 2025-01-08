from pydantic import BaseModel
from typing import List  # Import List từ typing

class ImageBase(BaseModel):
    url: str
    public_id: str

    class Config:
        from_attributes = True

class ImageRequest(BaseModel):  # Kế thừa từ BaseModel
    imgase: List[ImageBase]  # Sử dụng List từ typing để khai báo danh sách

    class Config:
        from_attributes = True

class ImageResponse(BaseModel):  # Kế thừa từ BaseModel
    imgase: List[ImageBase]  # Sử dụng List từ typing để khai báo danh sách

    class Config:
        from_attributes = True
