from typing import List

from app.auth.oauth2 import get_current_user
from app.database import get_db
from app.user import models
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from . import crud, schemas

router = APIRouter(
    prefix="/messages",
    tags=["messages"],
)


@router.get("/messages", response_model=List[schemas.MessageResponse])
async def get_messages(
    db: AsyncSession = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    messages = await crud.get_messages(db, current_user.id)
    return messages


@router.post("/message/")
async def post_message(
    message: schemas.MessageCreate,
    db: AsyncSession = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    user_message, gpt_message = await crud.create_message(
        db, current_user.id, message
    )
    return {
        "user_message": user_message.content,
        "gpt_response": gpt_message.content,
    }
