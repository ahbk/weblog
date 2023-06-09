import argparse
import asyncio
from pydantic import EmailStr

from weblog.db import users, meta, models

parser = argparse.ArgumentParser(description="Create a user")

parser.add_argument("email", type=EmailStr, help="email")
parser.add_argument("password", type=str, help="password")
parser.add_argument("--is-superuser", action="store_true", help="is superuser")

args = parser.parse_args()


async def create_user(args) -> models.User:
    async with meta.async_session() as session:
        return await users.create_user(
            session, args.email, args.password, args.is_superuser
        )


user = asyncio.run(create_user(args))
if user:
    print(user.id)
