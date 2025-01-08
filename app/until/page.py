from pydantic import BaseModel, Field
from typing import Optional, TypeVar, Generic, Sequence
from app.schemas.sche_base import MetadataSchema
from app.schemas.sche_page import PaginationParams
from sqlalchemy.orm import Query
from sqlalchemy import asc, desc
from app.until.exception_handler import CustomException

T = TypeVar("T")


class Page(MetadataSchema, Generic[T]):
    metadata: Sequence[T]


def paginate(model,model_response, query: Query, params: Optional[PaginationParams]) -> "Page[T]":
    try:
        total = query.count()

        if params.order:
            direction = desc if params.order == "desc" else asc
            query = query.order_by(direction(getattr(model, params.sort_by)))

        data = (
            query.limit(params.page_size)
            .offset(params.page_size * (params.page - 1))
            .all()
        )
        data_response=[ model_response(de) for de in data]
        return Page(
            total_items=total,
            current_page=params.page,
            page_size=params.page_size,
            total_pages=(total+params.page_size-1)//params.page_size,
            metadata=data_response,
        )

    except Exception as e:
        raise CustomException(http_code=500, code="500", message=str(e))
