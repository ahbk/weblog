import argparse
import asyncio
import weblog.db.users
from pydantic import EmailStr

parser = argparse.ArgumentParser(description="Create a user")

parser.add_argument("email", type=EmailStr, help="email")
parser.add_argument("password", type=str, help="password")
parser.add_argument("--is-superuser", action="store_true", help="is superuser")

args = parser.parse_args()

result = asyncio.run(
    weblog.db.users.create_user(args.email, args.password, args.is_superuser)
)
print(result)
