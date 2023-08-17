from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from weblog.db import meta, models, posts, schemas, users

router = APIRouter()


@router.post("/create", response_model=schemas.PostRead, tags=["posts"])
async def create(
    post: schemas.PostCreate,
    user: models.User = Depends(users.active_verified_user),
    session: AsyncSession = Depends(meta.get_async_session),
):
    return await posts.create(session, post=post, author_id=user.id)


@router.get("/list", response_model=list[schemas.PostRead], tags=["posts"])
async def list(
    skip: int = 0,
    limit: int = 10,
    session: AsyncSession = Depends(meta.get_async_session),
):
    post_list = await posts.list(session, skip=skip, limit=limit)
    return post_list


@router.get("/get/{post_id}", response_model=schemas.PostRead, tags=["posts"])
async def get(post_id: int, session: AsyncSession = Depends(meta.get_async_session)):
    post = await posts.get(session, post_id=post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post


@router.delete("/delete/{post_id}", tags=["posts"])
async def delete(
    post_id: int,
    session: AsyncSession = Depends(meta.get_async_session),
    _: models.User = Depends(users.active_verified_user),
):
    return await posts.delete(session, post_id=post_id)


@router.patch("/update/{post_id}", tags=["posts"])
async def update(
    post_id: int,
    post: schemas.PostUpdate,
    _: models.User = Depends(users.active_verified_user),
    session: AsyncSession = Depends(meta.get_async_session),
):
    values = post.dict(exclude_unset=True)
    return await posts.update(session, post_id=post_id, values=values)
