from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.base import Base

from .abc import AbstractRepository


class Repository[TModel: Base](AbstractRepository):
    def __init__(self, session: AsyncSession, model: type[TModel]):
        self._session = session
        self._model = model

    def add(self, entity: TModel) -> None:
        self._session.add(entity)

    async def get(self, id: int) -> TModel:
        stmt = select(self._model).where(self._model.id == id)
        result = await self._session.execute(stmt)
        return result.scalar_one()

    async def remove(self, id: int) -> None:
        stmt = delete(self._model).where(self._model.id == id)
        await self._session.execute(stmt)
