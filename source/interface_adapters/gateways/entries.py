from abc import ABC, abstractmethod
from dataclasses import dataclass

from entities import entry
from sqlalchemy.ext.asyncio import AsyncSession


class Database(ABC):
    @abstractmethod
    async def insert(
        self,
        entry_models: list[entry.Model],
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
