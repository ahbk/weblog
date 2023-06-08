from fastapi import APIRouter, Depends, HTTPException

from . import schemas, crud, users, models

posts = APIRouter()


@posts.post("/create", response_model=schemas.PostRead, tags=["posts"])
async def create_post(
    post: schemas.PostCreate,
    user: models.User = Depends(users.current_active_superuser),
):
    return await crud.create_post(post=post)


@posts.get("/list", response_model=list[schemas.PostRead], tags=["posts"])
async def read_posts(skip: int = 0, limit: int = 10):
    posts = await crud.get_posts(skip=skip, limit=limit)
    return posts


@posts.get("/get/{post_id}", response_model=schemas.PostRead, tags=["posts"])
async def read_post(post_id: int):
    post = await crud.get_post(post_id=post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post


@posts.delete("/delete/{post_id}", tags=["posts"])
async def delete_post(post_id: int):
    return await crud.delete_post(post_id=post_id)


@posts.patch("/update/{post_id}", tags=["posts"])
async def update_post(post_id: int, post: schemas.PostUpdate):
    values = post.dict(exclude_unset=True)
    return await crud.update_post(post_id, values)
