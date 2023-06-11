import datetime
from typing import List, Optional

from fastapi_users.db import SQLAlchemyBaseUserTableUUID
from fastapi_users_db_sqlalchemy.access_token import SQLAlchemyBaseAccessTokenTableUUID
from sqlalchemy import ForeignKey, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from weblog.db import meta


class User(SQLAlchemyBaseUserTableUUID, meta.Base):
    display_name: Mapped[Optional[str]] = mapped_column(String(30))
    posts: Mapped[List["Post"]] = relationship(
        back_populates="author",
    )


class AccessToken(SQLAlchemyBaseAccessTokenTableUUID, meta.Base):
    pass


class Post(meta.Base):
    __tablename__ = "post"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(30))
    body: Mapped[Optional[str]] = mapped_column(Text)
    author_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    author: Mapped["User"] = relationship(back_populates="posts")
    created: Mapped[datetime.datetime] = mapped_column(
        server_default=func.CURRENT_TIMESTAMP()
    )

    def __repr__(self) -> str:
        return f"Post(id={self.id!r}, title={self.title!r}, body={self.body!r}, created={self.created!r})"
