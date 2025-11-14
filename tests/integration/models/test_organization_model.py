import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from tests.utils import (
    connect_activity_and_organization,
    create_activity,
    create_building,
    create_city,
    create_organization,
    create_street,
    get_organization,
)


@pytest.mark.asyncio
@pytest.mark.usefixtures('clean_db')
class TestOrganizationModel:
    async def test_activity_organization_association(self, pg_session: AsyncSession):
        await create_activity(pg_session, 'Delivery')
        await create_city(pg_session, 'Moscow')
        await create_street(pg_session, 1, 'Tverskaya')
        await create_building(pg_session, 1, '16', 'office 4', 55.764551, 37.606406)
        await create_organization(pg_session, 'Yandex Eats', 1)
        await connect_activity_and_organization(pg_session, 1, 1)

        organization = await get_organization(pg_session, 1)
        assert organization.name == 'Yandex Eats'
        assert organization.building_id == 1
        assert organization.activities[0].name == 'Delivery'
