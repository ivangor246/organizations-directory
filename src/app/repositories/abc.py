from abc import ABC, abstractmethod


class AbstractRepository[TModel](ABC):
    @abstractmethod
    def add(self, entity: TModel) -> None: ...

    @abstractmethod
    async def get(self, id: int) -> TModel: ...

    @abstractmethod
    async def remove(self, id: int) -> None: ...
