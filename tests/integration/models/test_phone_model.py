import pytest
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from tests.utils import (
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
    await create_organization(pg_session, 'Yandex Eats', 1)


@pytest.mark.asyncio
@pytest.mark.usefixtures('clean_db')
class TestPhoneModel:
    async def test_phone_number_constraint(self, pg_session: AsyncSession):
        await create_related_models(pg_session)
        await create_phone(pg_session, '+7 999 999 99 99', 1)

        with pytest.raises(IntegrityError):
            await create_phone(pg_session, '+7 999 999 99 99', 1)

    async def test_phone_organization_association(self, pg_session: AsyncSession):
        await create_related_models(pg_session)
        await create_phone(pg_session, '+7 999 999 99 99', 1)
        await create_phone(pg_session, '+7 111 111 11 11', 1)

        organization = await get_organization(pg_session, 1)
        numbers = {p.number for p in organization.phones}
        assert numbers == {'+7 999 999 99 99', '+7 111 111 11 11'}
