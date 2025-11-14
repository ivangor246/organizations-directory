from sqlalchemy.ext.asyncio import AsyncSession

from app.models.cities import City

from .base import Repository


class CityRepository(Repository[City]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, City)

    def add(self, city: City) -> None:
        super().add(city)
