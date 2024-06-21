from abc import ABC, abstractmethod
from dataclasses import dataclass
from uuid import UUID

from entities import entry
from sqlalchemy.engine.result import ScalarResult
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import delete, select


class Database(ABC):
    @abstractmethod
    async def insert(
        self,
        entry_models: list[entry.Model],
    ) -> None: ...

    @abstractmethod
    async def select(self) -> ScalarResult[entry.Model]: ...

    @abstractmethod
    async def delete(
        self,
        entry_uuids: list[UUID],
    ) -> None: ...


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

    async def delete(
        self,
        entry_uuids: list[UUID],
    ):
        await self.session.execute(
            statement=delete(entry.Model).where(entry.Model.uuid.in_(entry_uuids))
        )
