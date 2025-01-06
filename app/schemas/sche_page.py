from pydantic import BaseModel, conint
from typing import Optional
from enum import Enum
from app.until.enums import OrderBy,generate_enum_from_model,UserFieldsEnum
from app.model.models import User
class PaginationParams(BaseModel):
    page_size: Optional[conint(gt=0, lt=1001)] = 10
    page: Optional[conint(gt=0)] = 1
    sort_by: Optional[UserFieldsEnum] = UserFieldsEnum.id
    order: Optional[OrderBy] = OrderBy.ASC
