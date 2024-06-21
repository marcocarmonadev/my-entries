from abc import ABC, abstractmethod
from dataclasses import dataclass
from uuid import UUID

from dateutil.relativedelta import relativedelta
from entities import entry
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import select


class Database(ABC):
    @abstractmethod
    async def select_by_uuid(
        self,
        uuid: UUID,
    ) -> entry.Model: ...

    @abstractmethod
    async def update_status(
        self,
        uuid: UUID,
        status: entry.Status,
    ) -> None: ...


@dataclass
class DatabaseImp(Database):
    session: "AsyncSession"

    async def select_by_uuid(
        self,
        uuid: UUID,
    ) -> entry.Model:
        if not (
            entry_model := await self.session.scalar(
                statement=select(entry.Model).where(entry.Model.uuid == uuid),
            )
        ):
            raise
        return entry_model

    async def update_status(
        self,
        uuid: UUID,
        status: entry.Status,
    ) -> None:
        entry_model = await self.select_by_uuid(uuid)
        if entry_model.status != status:
            entry_model.status = status
            if entry_model.repeat_forever and not entry_model.repeated:
                entry_model.repeated = True
                self.session.add(
                    entry.Model(
                        concept=entry_model.concept,
                        amount=entry_model.amount,
                        due_date=entry_model.due_date
                        + relativedelta(
                            months=1 * (entry_model.repeat_interval or 1),
                        ),
                        status=entry.Status.PENDING,
                        repeat_forever=True,
                        repeated=False,
                        repeat_interval=entry_model.repeat_interval,
                    )
                )
