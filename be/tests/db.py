import unittest
import asyncio
from unittest import IsolatedAsyncioTestCase
from weblog.db.meta import async_engine
from weblog.db.models import Base, Post

from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy import text, select


shared = {'resource': None}

async def immediate_task():
    print('immediate task')
    shared['resource'] = await asyncio.sleep(0, 1)

async def fast_task():
    print('fast task')
    shared['resource'] = await asyncio.sleep(.1, 2)

async def slow_task():
    print('slow task')
    shared['resource'] = await asyncio.sleep(1, 3)

async def task_runner():
    await slow_task()
    await fast_task()
    await immediate_task()


class TestAsyncLab(IsolatedAsyncioTestCase):
    async def test_1(self):
        await task_runner()
        self.assertEqual(3, shared['resource'])

@unittest.skip("temporarily disabled")
class TestDB(IsolatedAsyncioTestCase):

    async def asyncSetUp(self):
        self._async_session = async_sessionmaker(async_engine, expire_on_commit=False)


    async def test_create_tables(self):

        async with async_engine.begin() as conn:
            await conn.execute(text("DROP TABLE posts"))
            await conn.run_sync(Base.metadata.create_all)

        p1 = Post(title="Hello world!", body="Lorem Ipsum...")
        p2 = Post(title="Hello again!", body="Lorem Ipsum...")

        async with self._async_session() as session:
            async with session.begin():
                session.add_all([p1, p2])

        async with self._async_session() as session:
            stmt = select(Post)
            result = await session.execute(stmt)

        self.assertEqual("Hello world!", result.first()[0].title)


    async def asyncTearDown(self):
        await async_engine.dispose()


if __name__ == '__main__':
    unittest.main()
