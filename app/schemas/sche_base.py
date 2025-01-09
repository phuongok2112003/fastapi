from pydantic import BaseModel
from typing import TypeVar, Generic, Optional

T = TypeVar("T")

class DataResponse(BaseModel, Generic[T]):
    code: str = '000'
    message: str = 'Thành công'
    data: Optional[T] = None  # Generic

    class Config:
        arbitrary_types_allowed = True

    def custom_response(self, code: str, message: str, data: T) -> "DataResponse[T]":
        # Trả về một đối tượng DataResponse mới thay vì thay đổi đối tượng hiện tại
        return DataResponse[T](code=code, message=message, data=data)

    def success_response(self, data: T) -> "DataResponse[T]":
        # Trả về đối tượng DataResponse với trạng thái thành công
        return DataResponse[T](code='200', message='Thành công', data=data)

class MetadataSchema(BaseModel):
    current_page: int
    page_size: int
    total_items: int
    total_pages: int
