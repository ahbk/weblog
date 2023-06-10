from fastapi import Depends, APIRouter

from weblog.db.models import User
from weblog.db.schemas import UserCreate, UserRead, UserUpdate
from weblog.db.users import auth_backend, current_active_user, fastapi_users

auth_router = APIRouter()
user_router = APIRouter()

auth_router.include_router(fastapi_users.get_auth_router(auth_backend))
auth_router.include_router(fastapi_users.get_register_router(UserRead, UserCreate))
auth_router.include_router(fastapi_users.get_reset_password_router())
auth_router.include_router(fastapi_users.get_verify_router(UserRead))

user_router.include_router(fastapi_users.get_users_router(UserRead, UserUpdate))


@user_router.get("/authenticated-route")
async def authenticated_route(user: User = Depends(current_active_user)):
    return {"message": f"Hello {user.email}!"}
