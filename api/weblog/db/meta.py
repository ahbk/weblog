import os
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import declarative_base

from weblog.config import settings

url = f"postgresql+asyncpg://{settings.db_uri}/weblog"
url_test = f"postgresql+asyncpg://{settings.db_uri}/weblog_test"

engine = create_async_engine(url)
engine_test = create_async_engine(url_test, echo=True)

async_session = async_sessionmaker(engine, expire_on_commit=False)
async_session_test = async_sessionmaker(engine_test, expire_on_commit=False)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session


async def get_async_session_test() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_test() as session:
        yield session


Base = declarative_base()
