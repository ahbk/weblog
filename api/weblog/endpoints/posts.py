from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from weblog.db import schemas, crud, users, models, meta

router = APIRouter()


@router.post("/create", response_model=schemas.PostRead, tags=["posts"])
async def create_post(
    post: schemas.PostCreate,
    user: models.User = Depends(users.current_active_superuser),
    session: AsyncSession = Depends(meta.get_async_session),
):
    return await crud.create_post(session, post=post, author_id=user.id)


@router.get("/list", response_model=list[schemas.PostRead], tags=["posts"])
async def read_posts(
    skip: int = 0,
    limit: int = 10,
    session: AsyncSession = Depends(meta.get_async_session),
):
    posts = await crud.get_posts(session, skip=skip, limit=limit)
    return posts


@router.get("/get/{post_id}", response_model=schemas.PostRead, tags=["posts"])
async def read_post(
    post_id: int, session: AsyncSession = Depends(meta.get_async_session)
):
    post = await crud.get_post(session, post_id=post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post


@router.delete("/delete/{post_id}", tags=["posts"])
async def delete_post(
    post_id: int, session: AsyncSession = Depends(meta.get_async_session)
):
    return await crud.delete_post(session, post_id=post_id)


@router.patch("/update/{post_id}", tags=["posts"])
async def update_post(
    post_id: int,
    post: schemas.PostUpdate,
    session: AsyncSession = Depends(meta.get_async_session),
):
    values = post.dict(exclude_unset=True)
    return await crud.update_post(session, post_id=post_id, values=values)
