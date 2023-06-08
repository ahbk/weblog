import datetime
from typing import Optional

from sqlalchemy import Text
from sqlalchemy import String
from sqlalchemy import func

from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import Depends
from fastapi_users.db import SQLAlchemyBaseUserTableUUID, SQLAlchemyUserDatabase
from fastapi_users_db_sqlalchemy.access_token import (
    SQLAlchemyAccessTokenDatabase,
    SQLAlchemyBaseAccessTokenTableUUID,
)

from weblog.db.meta import get_async_session


class Base(DeclarativeBase):
    pass


class User(SQLAlchemyBaseUserTableUUID, Base):
    pass


class AccessToken(SQLAlchemyBaseAccessTokenTableUUID, Base):
    pass


class Post(Base):
    __tablename__ = "post"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(30))
    body: Mapped[Optional[str]] = mapped_column(Text)
    created: Mapped[datetime.datetime] = mapped_column(
        server_default=func.CURRENT_TIMESTAMP()
    )

    def __repr__(self) -> str:
        return f"Post(id={self.id!r}, title={self.title!r}, body={self.body!r}, created={self.created!r})"


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)


async def get_access_token_db(
    session: AsyncSession = Depends(get_async_session),
):
    yield SQLAlchemyAccessTokenDatabase(session, AccessToken)
