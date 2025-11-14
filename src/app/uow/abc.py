from __future__ import annotations

from abc import ABC, abstractmethod

from app.repositories.base import AbstractRepository


class AbstractUnitOfWork(ABC):
    activities: AbstractRepository
    buildings: AbstractRepository
    cities: AbstractRepository
    organizations: AbstractRepository
    phones: AbstractRepository
    streets: AbstractRepository

    async def __aenter__(self) -> AbstractUnitOfWork:
        return self

    async def __aexit__(self, *args) -> None:
        await self.rollback()

    @abstractmethod
    async def commit(self) -> None: ...

    @abstractmethod
    async def rollback(self) -> None: ...
