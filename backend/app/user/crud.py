from app.auth.hash_password import HashPassword
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from . import models, schemas


async def get_user(db: AsyncSession, username: str):
    result = await db.execute(
        select(models.User).filter(models.User.username == username)
    )
    return result.scalar_one_or_none()


async def create_user(db: AsyncSession, request: schemas.UserCreate):
    existing_user = await db.execute(
        select(models.User).filter(models.User.username == request.username)
    )
    existing_user = existing_user.scalars().first()

    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")

    new_user = models.User(username=request.username)
    new_user.password = HashPassword.bcrypt(request.password)

    db.add(new_user)
    await db.flush()
    await db.commit()
    await db.refresh(new_user)
    return new_user


async def check_user_exists(db: AsyncSession, user_id: int) -> bool:
    result = await db.execute(
        select(models.User).filter(models.User.id == user_id)
    )
    return result.scalars().first() is not None
