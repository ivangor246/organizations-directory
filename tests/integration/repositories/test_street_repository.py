import pytest
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.streets import Street
from app.repositories.streets import StreetRepository
from tests.utils import create_city, create_street, get_street


@pytest.mark.asyncio
@pytest.mark.usefixtures('clean_db')
class TestStreetRepository:
    async def test_add_street(self, pg_session: AsyncSession):
        repo = StreetRepository(pg_session)
        await create_city(pg_session, 'Moscow')

        street = Street(name='Tverskaya', city_id=1)
        repo.add(street)
        await pg_session.commit()

        retrieved = await get_street(pg_session, 1)
        assert retrieved.name == 'Tverskaya'
        assert retrieved.city_id == 1

    async def test_get_street(self, pg_session: AsyncSession):
        repo = StreetRepository(pg_session)
        await create_city(pg_session, 'Moscow')
        await create_street(pg_session, 1, 'Tverskaya')

        retrieved = await repo.get(1)
        assert retrieved.name == 'Tverskaya'
        assert retrieved.city_id == 1

    async def test_remove_street(self, pg_session: AsyncSession):
        repo = StreetRepository(pg_session)
        await create_city(pg_session, 'Moscow')
        await create_street(pg_session, 1, 'Tverskaya')

        await repo.remove(1)

        with pytest.raises(NoResultFound):
            await get_street(pg_session, 1)
