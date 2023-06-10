from typing import Sequence, Optional
import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession

from . import models, schemas


async def get(session: AsyncSession, post_id: int) -> Optional[models.Post]:
    statement = (
        sa.select(models.Post).join(models.Post.author).where(models.Post.id == post_id)
    )
    result = await session.scalars(statement)
    return result.first()


async def list(session: AsyncSession, skip: int, limit: int) -> Sequence[models.Post]:
    statement = (
        sa.select(models.Post)
        .offset(skip)
        .limit(limit)
        .order_by(models.Post.created.desc())
    )
    result = await session.scalars(statement)
    return result.all()


async def create(
    session: AsyncSession, post: schemas.PostCreate, author_id
) -> models.Post:
    db_post = models.Post(title=post.title, body=post.body, author_id=author_id)
    session.add(db_post)
    await session.commit()
    return db_post


async def delete(session: AsyncSession, post_id: int) -> sa.Result:
    statement = sa.delete(models.Post).where(models.Post.id == post_id)
    result = await session.execute(statement)
    await session.commit()
    return result


async def update(session: AsyncSession, post_id: int, values) -> sa.Result:
    statement = sa.update(models.Post).where(models.Post.id == post_id).values(**values)
    result = await session.execute(statement)
    await session.commit()
    return result
