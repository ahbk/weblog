import argparse
import asyncio

from weblog.db import meta, models, users

parser = argparse.ArgumentParser(
    prog="create_user", description="Create a user", epilog="Have fun!"
)

parser.add_argument("email", type=str, help="email")
parser.add_argument("password", type=str, help="password")
parser.add_argument("-d", "--display-name", type=str, help="display name")
parser.add_argument("--is-superuser", action="store_true", help="is superuser")
parser.add_argument("--is-verified", action="store_true", help="is verified")

args = parser.parse_args()


async def create_user(args) -> models.User:
    async with meta.async_session() as session:
        return await users.create_user(
            session,
            args.email,
            args.password,
            args.display_name,
            args.is_superuser,
            args.is_verified,
        )


user = asyncio.run(create_user(args))
