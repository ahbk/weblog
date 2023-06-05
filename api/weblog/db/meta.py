from sqlalchemy.ext.asyncio import create_async_engine
import os

port = os.getenv("POSTGRES_PORT", "5439")

engine = create_async_engine(
    f"postgresql+asyncpg://{os.environ['POSTGRES_USER']}:{os.environ['POSTGRES_PASSWORD']}@{os.environ['POSTGRES_HOST']}:{port}/weblog",
    echo=True,
)
engine_test = create_async_engine(
    f"postgresql+asyncpg://{os.environ['POSTGRES_USER']}:{os.environ['POSTGRES_PASSWORD']}@{os.environ['POSTGRES_HOST']}:{port}/weblog_test",
    echo=True,
)
