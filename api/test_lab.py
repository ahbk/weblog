import asyncio
import unittest

from pydantic import EmailStr
from sqlalchemy import select

from weblog.db import meta, models, users


def test_test():
    assert True


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
        self.session = meta.async_session_test

    async def test_crud_posts(self):
        # wipe and recreate
        async with meta.engine_test.begin() as conn:
            await conn.run_sync(meta.Base.metadata.drop_all)
            await conn.run_sync(meta.Base.metadata.create_all)

        async with self.session() as session:
            user = await users.create_user(session, EmailStr("a@a.a"), "a", False)

        assert user is not None

        # add sample data
        p1 = models.Post(title="Hello world!", body="Lorem Ipsum...", author_id=user.id)
        p2 = models.Post(title="Hello again!", body="Lorem Ipsum...", author_id=user.id)

        async with self.session() as session:
            async with session.begin():
                session.add_all([p1, p2])

        # select all
        async with self.session() as session:
            stmt = select(models.Post)
            result = await session.execute(stmt)

        first_row = result.first()

        # p1.title
        self.assertEqual("Hello world!", first_row[0].title if first_row else None)

    async def asyncTearDown(self):
        await meta.engine_test.dispose()


if __name__ == "__main__":
    unittest.main()
