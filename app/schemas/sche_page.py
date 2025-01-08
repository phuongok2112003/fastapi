from pydantic import BaseModel, conint
from typing import Optional
from enum import Enum
from app.until.enums import OrderBy,generate_enum_from_model
from app.model.models import User
# UserFieldsEnum = generate_enum_from_model(User)
class PaginationParams(BaseModel):
    page_size: Optional[conint(gt=0, lt=1001)] = 10
    page: Optional[conint(gt=0)] = 1
    sort_by: Optional[str] = "id"
    order: Optional[OrderBy] = OrderBy.ASC
