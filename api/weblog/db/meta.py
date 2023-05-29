from sqlalchemy.ext.asyncio import create_async_engine
import os

engine = create_async_engine(
    f"postgresql+asyncpg://{os.environ['POSTGRES_USER']}:{os.environ['POSTGRES_PASSWORD']}@{os.environ['POSTGRES_HOST']}:5432/weblog",
    echo=True,
)
engine_test = create_async_engine(
    f"postgresql+asyncpg://{os.environ['POSTGRES_USER']}:{os.environ['POSTGRES_PASSWORD']}@{os.environ['POSTGRES_HOST']}:5432/weblog_test",
    echo=True,
)
