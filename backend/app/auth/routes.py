from app.auth.hash_password import HashPassword
from app.database import get_db
from app.user import crud
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from . import oauth2

router = APIRouter(
    tags=["authentication"],
)


@router.post("/token")
async def get_token(
    request: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db),
):
    user = await crud.get_user(db, username=request.username)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Invalid credentials"
        )
    if not HashPassword.verify(user.password, request.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Wrong password"
        )

    access_token = oauth2.create_access_token(data={"username": user.username})

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_name": user.username,
    }
