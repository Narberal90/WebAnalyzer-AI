from app.database import get_db
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from . import crud, schemas

router = APIRouter(
    prefix="/user",
    tags=["user"],
)


@router.post("/register", response_model=schemas.UserOut)
async def create_user(
    request: schemas.UserCreate, db: AsyncSession = Depends(get_db)
):
    return await crud.create_user(db, request)
