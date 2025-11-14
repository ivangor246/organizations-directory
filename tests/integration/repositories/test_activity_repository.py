import pytest
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.activities import Activity
from app.repositories.activities import ActivityRepository
from tests.utils import create_activity, get_activity


@pytest.mark.asyncio
@pytest.mark.usefixtures('clean_db')
class TestActivityRepository:
    async def test_add_activity(self, pg_session: AsyncSession):
        repo = ActivityRepository(pg_session)

        activity = Activity(name='Delivery', depth=0, parent_id=None)
        repo.add(activity)
        await pg_session.commit()

        retrieved = await get_activity(pg_session, 1)
        assert retrieved.name == 'Delivery'
        assert retrieved.depth == 0
        assert retrieved.parent_id is None

    async def test_get_activity(self, pg_session: AsyncSession):
        repo = ActivityRepository(pg_session)
        await create_activity(pg_session, 'Delivery')

        retrieved = await repo.get(1)
        assert retrieved.name == 'Delivery'

    async def test_remove_activity(self, pg_session: AsyncSession):
        repo = ActivityRepository(pg_session)
        await create_activity(pg_session, 'Delivery')

        await repo.remove(1)

        with pytest.raises(NoResultFound):
            await get_activity(pg_session, 1)
