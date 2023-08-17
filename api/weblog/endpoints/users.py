from fastapi import APIRouter, Depends

from weblog.db import models, users, schemas

auth_router = APIRouter()
user_router = APIRouter()

auth_router.include_router(users.fastapi_users.get_auth_router(users.auth_backend))
auth_router.include_router(
    users.fastapi_users.get_register_router(schemas.UserRead, schemas.UserCreate)
)
auth_router.include_router(users.fastapi_users.get_reset_password_router())
auth_router.include_router(users.fastapi_users.get_verify_router(schemas.UserRead))

user_router.include_router(
    users.fastapi_users.get_users_router(schemas.UserRead, schemas.UserUpdate)
)


@user_router.get("/authenticated-route")
async def authenticated_route(user: models.User = Depends(users.active_user)):
    return {"message": f"Hello {user.email}!"}
