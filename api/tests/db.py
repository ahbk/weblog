import unittest
import asyncio
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy import text, select

from weblog.db.meta import engine_test
from weblog.db.models import Base, Post


# reminder how async works
class TestAsyncLab(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.shared = {"resource": 0}

    async def immediate_task(self):
        self.shared["resource"] = 1

    async def fast_task(self):
        self.shared["resource"] = await asyncio.sleep(0.1, 2)

    async def slow_task(self):
        self.shared["resource"] = await asyncio.sleep(1, 3)

    async def test_how_async_works(self):
        await asyncio.gather(self.slow_task(), self.fast_task(), self.immediate_task())
        self.assertEqual(3, self.shared["resource"])


# crud test on db
class TestDB(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self._async_session = async_sessionmaker(engine_test, expire_on_commit=False)

    async def test_crud_posts(self):
        # wipe and recreate
        async with engine_test.begin() as conn:
            await conn.execute(text("DROP TABLE IF EXISTS posts"))
            await conn.run_sync(Base.metadata.create_all)

        # add sample data
        p1 = Post(title="Hello world!", body="Lorem Ipsum...")
        p2 = Post(title="Hello again!", body="Lorem Ipsum...")

        async with self._async_session() as session:
            async with session.begin():
                session.add_all([p1, p2])

        # select all
        async with self._async_session() as session:
            stmt = select(Post)
            result = await session.execute(stmt)

        first_row = result.first()

        # p1.title
        self.assertEqual("Hello world!", first_row[0].title if first_row else None)

    async def asyncTearDown(self):
        await engine_test.dispose()


if __name__ == "__main__":
    unittest.main()
