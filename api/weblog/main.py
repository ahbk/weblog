from typing import Union
import uvicorn

from fastapi import Depends, FastAPI

from weblog.db.models import User
from weblog.db.schemas import UserCreate, UserRead, UserUpdate
from weblog.db.users import auth_backend, current_active_user, fastapi_users
from weblog.db import routers

app = FastAPI()

app.include_router(
    routers.posts,
    prefix="/posts",
    tags=["posts"],
)

app.include_router(
    fastapi_users.get_auth_router(auth_backend), prefix="/auth", tags=["auth"]
)
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)


@app.get("/authenticated-route")
async def authenticated_route(user: User = Depends(current_active_user)):
    return {"message": f"Hello {user.email}!"}


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


def run():
    uvicorn.run("weblog.main:app", reload=True, host="0.0.0.0", log_level="info")
