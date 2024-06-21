from abc import ABC, abstractmethod
from dataclasses import dataclass

from entities import entry
from sqlalchemy.engine.result import ScalarResult
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import select


class Database(ABC):
    @abstractmethod
    async def insert(
        self,
        entry_models: list[entry.Model],
    ) -> None: ...

    @abstractmethod
    async def select(self) -> ScalarResult[entry.Model]: ...


@dataclass
class DatabaseImp(Database):
    session: "AsyncSession"

    async def insert(
        self,
        entry_models: list[entry.Model],
    ) -> None:
        async with self.session.begin_nested():
            self.session.add_all(entry_models)

    async def select(self) -> ScalarResult[entry.Model]:
        return await self.session.scalars(
            statement=select(entry.Model).order_by(entry.Model.due_date),
        )
