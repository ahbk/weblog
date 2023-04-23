from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import create_engine

async_engine = create_async_engine( "postgresql+asyncpg://postgres:asdf@localhost:5432/app", echo=True)
engine = create_engine( "postgresql+psycopg://postgres:asdf@localhost:5432/app", echo=True)
