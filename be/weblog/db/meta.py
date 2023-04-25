from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import create_engine
import os

engine = create_async_engine(
    f"postgresql+asyncpg://postgres:{os.environ['POSTGRES_PASSWORD']}@db:5432/weblog", echo=True
)
engine_test = create_async_engine(
    f"postgresql+psycopg://postgres:{os.environ['POSTGRES_PASSWORD']}@db:5432/weblog_test", echo=True
)
