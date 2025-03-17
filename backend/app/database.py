from app.config import settings
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

async_engine = create_async_engine(settings.ASYNC_DATABASE_URL, echo=True)
sync_engine = create_engine(settings.SYNC_DATABASE_URL, echo=True)


async_session = sessionmaker(
    async_engine, class_=AsyncSession, expire_on_commit=False
)

sync_session = sessionmaker(sync_engine)


async def get_db():
    async with async_session() as db:
        yield db


Base = declarative_base()
