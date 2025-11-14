import pytest
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.cities import City
from app.repositories.cities import CityRepository
from tests.utils import create_city, get_city


@pytest.mark.asyncio
@pytest.mark.usefixtures('clean_db')
class TestCityRepository:
    async def test_add_city(self, pg_session: AsyncSession):
        repo = CityRepository(pg_session)

        city = City(name='Moscow')
        repo.add(city)
        await pg_session.commit()

        retrieved = await get_city(pg_session, 1)
        assert retrieved.name == 'Moscow'

    async def test_get_city(self, pg_session: AsyncSession):
        repo = CityRepository(pg_session)

        await create_city(pg_session, 'Moscow')

        retrieved = await repo.get(1)
        assert retrieved.name == 'Moscow'

    async def test_remove_city(self, pg_session: AsyncSession):
        repo = CityRepository(pg_session)

        await create_city(pg_session, 'Moscow')
        await repo.remove(1)

        with pytest.raises(NoResultFound):
            await get_city(pg_session, 1)
