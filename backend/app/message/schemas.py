import datetime
from typing import List

from pydantic import BaseModel, Field


class MessageCreate(BaseModel):
    content: str = Field(..., min_length=1, max_length=5000)


class MessageResponse(BaseModel):
    id: int
    user_id: int
    content: str
    created_at: datetime.datetime

    class Config:
        from_attributes = True


class PaginatedMessageResponse(BaseModel):
    items: List[MessageResponse]
    total: int
    has_more: bool
