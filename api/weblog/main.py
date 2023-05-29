from typing import Union
import uvicorn
import os

from fastapi import FastAPI

from weblog.db.models import Post
from sqlalchemy import select

app = FastAPI()

SECRET = os.environ["SECRET_KEY"]


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


def run():
    uvicorn.run("weblog.main:app", reload=True, host="0.0.0.0", log_level="info")
