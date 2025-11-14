from sqlalchemy.ext.asyncio import AsyncSession

from app.models.buildings import Building

from .base import Repository


class BuildingRepository(Repository[Building]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Building)

    def add(self, building: Building) -> None:
        super().add(building)
