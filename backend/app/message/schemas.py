import datetime
from pydantic import BaseModel


class MessageCreate(BaseModel):
    content: str


class MessageResponse(BaseModel):
    id: int
    user_id: int
    content: str
    created_at: datetime.datetime

    class Config:
        from_attributes = True
