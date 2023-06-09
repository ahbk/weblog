from fastapi import Depends, APIRouter

from weblog.db.models import User
from weblog.db.schemas import UserCreate, UserRead, UserUpdate
from weblog.db.users import auth_backend, current_active_user, fastapi_users

router_auth = APIRouter()
router_user = APIRouter()

router_auth.include_router(fastapi_users.get_auth_router(auth_backend))
router_auth.include_router(fastapi_users.get_register_router(UserRead, UserCreate))
router_auth.include_router(fastapi_users.get_reset_password_router())
router_auth.include_router(fastapi_users.get_verify_router(UserRead))

router_user.include_router(fastapi_users.get_users_router(UserRead, UserUpdate))


@router_user.get("/authenticated-route")
async def authenticated_route(user: User = Depends(current_active_user)):
    return {"message": f"Hello {user.email}!"}
