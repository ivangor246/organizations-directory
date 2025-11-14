import pytest
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from tests.utils import create_building, create_city, create_street


@pytest.mark.asyncio
@pytest.mark.usefixtures('clean_db')
class TestStreetModel:
    async def test_name_city_constraint(self, pg_session: AsyncSession):
        await create_city(pg_session, 'Moscow')
        await create_street(pg_session, 1, 'Tverskaya')
        await create_building(pg_session, 1, '16', 'office 4', 55.764551, 37.606406)

        with pytest.raises(IntegrityError):
            await create_building(pg_session, 1, '16', 'apt 28', 56.841935, 37.325012)
