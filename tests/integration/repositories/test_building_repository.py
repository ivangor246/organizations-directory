import pytest
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.buildings import Building
from app.repositories.buildings import BuildingRepository
from tests.utils import create_building, create_city, create_street, get_building


@pytest.mark.asyncio
@pytest.mark.usefixtures('clean_db')
class TestBuildingRepository:
    async def test_add_building(self, pg_session: AsyncSession):
        repo = BuildingRepository(pg_session)
        await create_city(pg_session, 'Moscow')
        await create_street(pg_session, 1, 'Tverskaya')

        building = Building(street_id=1, number='16', detail='office 4', latitude=55.764551, longitude=37.606406)
        repo.add(building)
        await pg_session.commit()

        retrieved = await get_building(pg_session, 1)
        assert retrieved.street_id == 1
        assert retrieved.number == '16'
        assert retrieved.detail == 'office 4'
        assert retrieved.latitude == 55.764551
        assert retrieved.longitude == 37.606406

    async def test_get_building(self, pg_session: AsyncSession):
        repo = BuildingRepository(pg_session)
        await create_city(pg_session, 'Moscow')
        await create_street(pg_session, 1, 'Tverskaya')
        await create_building(pg_session, 1, '16', 'office 4', 55.764551, 37.606406)

        retrieved = await repo.get(1)
        assert retrieved.street_id == 1
        assert retrieved.number == '16'

    async def test_remove_building(self, pg_session: AsyncSession):
        repo = BuildingRepository(pg_session)
        await create_city(pg_session, 'Moscow')
        await create_street(pg_session, 1, 'Tverskaya')
        await create_building(pg_session, 1, '16', 'office 4', 55.764551, 37.606406)

        await repo.remove(1)

        with pytest.raises(NoResultFound):
            await get_building(pg_session, 1)
