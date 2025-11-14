import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from tests.utils import create_activity, get_activity


@pytest.mark.asyncio
@pytest.mark.usefixtures('clean_db')
class TestActivityModel:
    async def test_nested_activity(self, pg_session: AsyncSession):
        await create_activity(pg_session, 'Software development')
        await create_activity(pg_session, 'Delivery', 1)

        activity = await get_activity(pg_session, 2)
        assert activity.name == 'Delivery'
        assert activity.depth == 1
        assert activity.parent_id == 1
