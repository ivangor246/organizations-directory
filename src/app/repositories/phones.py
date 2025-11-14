from sqlalchemy.ext.asyncio import AsyncSession

from app.models.phones import Phone

from .base import Repository


class PhoneRepository(Repository[Phone]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Phone)

    def add(self, phone: Phone) -> None:
        super().add(phone)
