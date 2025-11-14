import pytest
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import async_sessionmaker

from app.models.cities import City
from app.uow.base import UnitOfWork
from tests.utils import get_city


@pytest.mark.asyncio
@pytest.mark.usefixtures('clean_db')
class TestUnitOfWork:
    async def test_uow_commit(self, pg_session_factory: async_sessionmaker):
        uow = UnitOfWork(pg_session_factory)

        async with uow:
            uow.cities.add(City(name='Moscow'))
            await uow.commit()

        async with pg_session_factory() as pg_session:
            retrieved = await get_city(pg_session, 1)
            assert retrieved.name == 'Moscow'

    async def test_uow_rollback(self, pg_session_factory: async_sessionmaker):
        uow = UnitOfWork(pg_session_factory)

        async with uow:
            uow.cities.add(City(name='Moscow'))
            await uow.rollback()

        async with pg_session_factory() as pg_session:
            with pytest.raises(NoResultFound):
                await get_city(pg_session, 1)

    async def test_uow_error_rollback(self, pg_session_factory: async_sessionmaker):
        uow = UnitOfWork(pg_session_factory)

        with pytest.raises(RuntimeError):
            async with uow:
                uow.cities.add(City(name='Moscow'))
                raise RuntimeError()

        async with pg_session_factory() as pg_session:
            with pytest.raises(NoResultFound):
                await get_city(pg_session, 1)
