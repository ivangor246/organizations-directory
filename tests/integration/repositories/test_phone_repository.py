import pytest
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.phones import Phone
from app.repositories.phones import PhoneRepository
from tests.utils import (
    create_building,
    create_city,
    create_organization,
    create_phone,
    create_street,
    get_phone,
)


async def create_related_models(pg_session: AsyncSession) -> None:
    await create_city(pg_session, 'Moscow')
    await create_street(pg_session, 1, 'Tverskaya')
    await create_building(pg_session, 1, '16', 'office 4', 55.764551, 37.606406)
    await create_organization(pg_session, 'Yandex Eats', 1)


@pytest.mark.asyncio
@pytest.mark.usefixtures('clean_db')
class TestPhoneRepository:
    async def test_add_phone(self, pg_session: AsyncSession):
        repo = PhoneRepository(pg_session)
        await create_related_models(pg_session)

        phone = Phone(number='+7 999 999 99 99', organization_id=1)
        repo.add(phone)
        await pg_session.commit()

        retrieved = await get_phone(pg_session, 1)
        assert retrieved.number == '+7 999 999 99 99'
        assert retrieved.organization_id == 1

    async def test_get_phone(self, pg_session: AsyncSession):
        repo = PhoneRepository(pg_session)
        await create_related_models(pg_session)
        await create_phone(pg_session, '+7 999 999 99 99', 1)

        retrieved = await repo.get(1)
        assert retrieved.number == '+7 999 999 99 99'
        assert retrieved.organization_id == 1

    async def test_remove_phone(self, pg_session: AsyncSession):
        repo = PhoneRepository(pg_session)
        await create_related_models(pg_session)
        await create_phone(pg_session, '+7 999 999 99 99', 1)

        await repo.remove(1)

        with pytest.raises(NoResultFound):
            await get_phone(pg_session, 1)
