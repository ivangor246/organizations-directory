import pytest
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.organizations import Organization
from app.repositories.organization import OrganizationRepository
from tests.utils import (
    create_activity,
    create_building,
    create_city,
    create_organization,
    create_phone,
    create_street,
    get_organization,
)


async def create_related_models(pg_session: AsyncSession) -> None:
    await create_city(pg_session, 'Moscow')
    await create_street(pg_session, 1, 'Tverskaya')
    await create_building(pg_session, 1, '16', 'office 4', 55.764551, 37.606406)


@pytest.mark.asyncio
@pytest.mark.usefixtures('clean_db')
class TestOrganizationRepository:
    async def test_add_organization(self, pg_session: AsyncSession):
        repo = OrganizationRepository(pg_session)
        await create_related_models(pg_session)

        organization = Organization(name='Yandex Eats', building_id=1)
        repo.add(organization)
        await pg_session.commit()

        retrieved = await get_organization(pg_session, 1)
        assert retrieved.name == 'Yandex Eats'

    async def test_get_organization(self, pg_session: AsyncSession):
        repo = OrganizationRepository(pg_session)
        await create_related_models(pg_session)
        await create_organization(pg_session, 'Yandex Eats', 1)

        retrieved = await repo.get(1)
        assert retrieved.name == 'Yandex Eats'
        assert retrieved.building_id == 1
        assert retrieved.building.number == '16'
        assert retrieved.activities == []
        assert retrieved.phones == []

    async def test_remove_organization(self, pg_session: AsyncSession):
        repo = OrganizationRepository(pg_session)
        await create_related_models(pg_session)
        await create_organization(pg_session, 'Yandex Eats', 1)

        await repo.remove(1)

        with pytest.raises(NoResultFound):
            await get_organization(pg_session, 1)

    async def test_associate_with_activities(self, pg_session: AsyncSession):
        repo = OrganizationRepository(pg_session)
        await create_related_models(pg_session)
        await create_activity(pg_session, 'Delivery')
        await create_activity(pg_session, 'Development')
        await create_organization(pg_session, 'Yandex', 1)

        await repo.associate_with_activity(1, 1)
        await repo.associate_with_activity(1, 2)

        retrieved = await get_organization(pg_session, 1)
        names = {a.name for a in retrieved.activities}
        assert names == {'Delivery', 'Development'}

    async def test_associate_with_phones(self, pg_session: AsyncSession):
        repo = OrganizationRepository(pg_session)
        await create_related_models(pg_session)
        await create_organization(pg_session, 'Yandex', 1)
        await create_phone(pg_session, '+7 999 999 99 99', 1)
        await create_phone(pg_session, '+7 111 111 11 11', 1)

        retrieved = await repo.get(1)
        numbers = {p.number for p in retrieved.phones}
        assert numbers == {'+7 999 999 99 99', '+7 111 111 11 11'}
