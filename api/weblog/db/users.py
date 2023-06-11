import contextlib
import os
import uuid
from typing import Optional

from fastapi import Depends, Request
from fastapi_users import BaseUserManager, FastAPIUsers, UUIDIDMixin
from fastapi_users.authentication import AuthenticationBackend, BearerTransport
from fastapi_users.authentication.strategy.db import (
    AccessTokenDatabase,
    DatabaseStrategy,
)
from fastapi_users.db import SQLAlchemyUserDatabase
from fastapi_users.exceptions import UserAlreadyExists
from fastapi_users_db_sqlalchemy.access_token import SQLAlchemyAccessTokenDatabase
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession

from weblog.db import meta, models, schemas, users

SECRET = os.environ["SECRET_KEY"]


async def get_user_db(session: AsyncSession = Depends(meta.get_async_session)):
    yield SQLAlchemyUserDatabase(session, models.User)


async def get_access_token_db(
    session: AsyncSession = Depends(meta.get_async_session),
):
    yield SQLAlchemyAccessTokenDatabase(session, models.AccessToken)


class UserManager(UUIDIDMixin, BaseUserManager[models.User, uuid.UUID]):
    reset_password_token_secret = SECRET
    verification_token_secret = SECRET

    async def on_after_register(
        self, user: models.User, request: Optional[Request] = None
    ):
        print(f"User {user.id} has registered.")

    async def on_after_forgot_password(
        self, user: models.User, token: str, request: Optional[Request] = None
    ):
        print(f"User {user.id} has forgot their password. Reset token: {token}")

    async def on_after_request_verify(
        self, user: models.User, token: str, request: Optional[Request] = None
    ):
        print(f"Verification requested for user {user.id}. Verification token: {token}")


async def get_user_manager(user_db: SQLAlchemyUserDatabase = Depends(get_user_db)):
    yield UserManager(user_db)


def get_database_strategy(
    access_token_db: AccessTokenDatabase[models.AccessToken] = Depends(
        get_access_token_db
    ),
) -> DatabaseStrategy:
    return DatabaseStrategy(access_token_db, lifetime_seconds=3600)


auth_backend = AuthenticationBackend(
    name="db",
    transport=BearerTransport(tokenUrl="auth/login"),
    get_strategy=get_database_strategy,
)

fastapi_users = FastAPIUsers[models.User, uuid.UUID](
    users.get_user_manager, [users.auth_backend]
)
current_active_user = fastapi_users.current_user(active=True)
current_active_superuser = fastapi_users.current_user(active=True, superuser=True)

get_user_db_context = contextlib.asynccontextmanager(users.get_user_db)
get_user_manager_context = contextlib.asynccontextmanager(users.get_user_manager)


async def create_user(
    session: AsyncSession, email: EmailStr, password: str, is_superuser: bool
) -> Optional[models.User]:
    try:
        async with get_user_db_context(session) as user_db:
            async with get_user_manager_context(user_db) as user_manager:
                user = await user_manager.create(
                    schemas.UserCreate(
                        email=email, password=password, is_superuser=is_superuser
                    )
                )
                return user
    except UserAlreadyExists:
        print(f"User {email} already exists")
