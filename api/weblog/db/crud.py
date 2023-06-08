from typing import Sequence, Optional
from sqlalchemy import select, delete, update
from sqlalchemy import Result

from . import models, schemas, database


async def get_post(post_id: int) -> Optional[models.Post]:
    statement = select(models.Post).where(models.Post.id == post_id)
    async with database.async_session() as session:
        result = await session.scalars(statement)
    return result.first()


async def get_posts(skip: int, limit: int) -> Sequence[models.Post]:
    statement = (
        select(models.Post)
        .offset(skip)
        .limit(limit)
        .order_by(models.Post.created.desc())
    )
    async with database.async_session() as session:
        result = await session.scalars(statement)
    return result.all()


async def create_post(post: schemas.PostCreate) -> models.Post:
    db_post = models.Post(title=post.title, body=post.body)
    async with database.async_session() as session:
        async with session.begin():
            session.add(db_post)
    return db_post


async def delete_post(post_id: int) -> Result:
    statement = delete(models.Post).where(models.Post.id == post_id)
    async with database.async_session() as session:
        async with session.begin():
            result = await session.execute(statement)
    return result


async def update_post(post_id: int, values) -> Result:
    statement = update(models.Post).where(models.Post.id == post_id).values(**values)
    async with database.async_session() as session:
        async with session.begin():
            result = await session.execute(statement)
    return result
