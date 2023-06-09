from typing import Union
import uvicorn
from fastapi import FastAPI
from weblog.endpoints import users, posts

app = FastAPI()

app.include_router(
    posts.router,
    prefix="/posts",
    tags=["posts"],
)

app.include_router(
    users.router_auth,
    prefix="/auth",
    tags=["auth"],
)

app.include_router(
    users.router_user,
    prefix="/user",
    tags=["user"],
)


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


def run():
    uvicorn.run("weblog.main:app", reload=True, host="0.0.0.0", log_level="info")
