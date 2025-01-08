from pydantic import BaseModel
from typing import Optional

class ImageBase(BaseModel):
    url : list[str]
    class Config:
        from_attributes=True

class ImageRequest(ImageBase):
    pass 
class ImageResponse(ImageBase):
    pass
