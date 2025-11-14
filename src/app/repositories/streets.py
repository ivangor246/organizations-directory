from sqlalchemy.ext.asyncio import AsyncSession

from app.models.streets import Street

from .base import Repository


class StreetRepository(Repository[Street]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Street)

    def add(self, street: Street) -> None:
        super().add(street)
