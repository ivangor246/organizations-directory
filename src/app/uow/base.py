from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.core.database import DEFAULT_SESSION_FACTORY
from app.repositories.activities import ActivityRepository
from app.repositories.buildings import BuildingRepository
from app.repositories.cities import CityRepository
from app.repositories.organization import OrganizationRepository
from app.repositories.phones import PhoneRepository
from app.repositories.streets import StreetRepository

from .abc import AbstractUnitOfWork


class UnitOfWork(AbstractUnitOfWork):
    activities: ActivityRepository
    buildings: BuildingRepository
    cities: CityRepository
    organizations: OrganizationRepository
    phones: PhoneRepository
    streets: StreetRepository

    _session: AsyncSession

    def __init__(self, session_factory: async_sessionmaker = DEFAULT_SESSION_FACTORY):
        self._session_factory = session_factory

    async def __aenter__(self) -> UnitOfWork:
        self._session = self._session_factory()

        self.activities = ActivityRepository(self._session)
        self.buildings = BuildingRepository(self._session)
        self.cities = CityRepository(self._session)
        self.organizations = OrganizationRepository(self._session)
        self.phones = PhoneRepository(self._session)
        self.streets = StreetRepository(self._session)

        return await super().__aenter__()

    async def __aexit__(self, *args) -> None:
        await super().__aexit__(*args)
        await self._session.close()

    async def commit(self) -> None:
        await self._session.commit()

    async def rollback(self) -> None:
        await self._session.rollback()
