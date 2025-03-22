from typing import List

from app.auth.oauth2 import get_current_user
from app.database import get_db
from app.user import models
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from . import crud, schemas

router = APIRouter(
    prefix="/messages",
    tags=["messages"],
)


@router.get("/", response_model=List[schemas.MessageResponse])
async def get_messages(
    db: AsyncSession = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
    skip: int = 0, limit: int = 10
):
    return await crud.get_messages(db, current_user.id, skip, limit)


@router.post(
    "/",
    response_model=List[schemas.MessageResponse],
    status_code=status.HTTP_201_CREATED,
)
async def post_message(
    message: schemas.MessageCreate,
    db: AsyncSession = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    user_msg, gpt_reply = await crud.create_message(
        db, current_user.id, message
    )

    return [user_msg, gpt_reply]
