import datetime
import uuid
from typing import Optional

from fastapi_users import schemas
from pydantic import BaseModel


class UserRead(schemas.BaseUser[uuid.UUID]):
    pass


class UserCreate(schemas.BaseUserCreate):
    pass


class UserUpdate(schemas.BaseUserUpdate):
    pass


class PostCreate(BaseModel):
    title: str
    body: str


class PostRead(BaseModel):
    id: int
    title: str
    body: str
    created: datetime.datetime
    author: UserRead

    class Config:
        from_attributes = True


class PostUpdate(BaseModel):
    id: Optional[int]
    title: Optional[str]
    body: Optional[str]
