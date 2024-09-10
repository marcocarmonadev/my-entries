import datetime as dt
from abc import ABC, abstractmethod
from dataclasses import dataclass
from uuid import UUID

from entities import entry
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import delete, select


class Database(ABC):
    @abstractmethod
    async def select_by_uuid(
        self,
        entry_uuid: UUID,
    ) -> entry.Model: ...

    @abstractmethod
    async def update(
        self,
        entry_uuid: UUID,
        entry_update_schema: entry.UpdateSchema,
    ) -> None: ...

    @abstractmethod
    async def delete(
        self,
        entry_uuid: UUID,
    ) -> None: ...

    @abstractmethod
    async def update_amount_inside_cajita(
        self,
        new_amount: float,
    ): ...


@dataclass
class DatabaseImp(Database):
    session: "AsyncSession"

    async def select_by_uuid(
        self,
        entry_uuid: UUID,
    ) -> entry.Model:
        if not (
            entry_model := await self.session.scalar(
                statement=select(entry.Model).where(entry.Model.uuid == entry_uuid),
            )
        ):
            raise
        return entry_model

    async def update(
        self,
        entry_uuid: UUID,
        entry_update_schema: entry.UpdateSchema,
    ) -> None:
        entry_model = await self.select_by_uuid(entry_uuid)
        for k, v in entry_update_schema.model_dump(
            exclude_unset=True,
        ).items():
            if k == "status" and entry_model.status != v:
                entry_model.status = v
                if entry_model.repeat_forever and not entry_model.repeated:
                    entry_model.repeated = True
                    self.session.add(
                        entry.Model(
                            concept=entry_model.concept,
                            amount=entry_model.amount,
                            due_date=entry.get_next_due_date(
                                date=entry_model.due_date,
                                frequency=entry_model.frequency,
                                repeat_interval=entry_model.repeat_interval,
                            ),
                            status=entry.Status.PENDING,
                            frequency=entry_model.frequency,
                            repeat_forever=True,
                            repeated=False,
                            repeat_interval=entry_model.repeat_interval,
                        )
                    )
            else:
                entry_model.__setattr__(k, v)

    async def delete(
        self,
        entry_uuid: UUID,
    ) -> None:
        await self.session.execute(
            statement=delete(entry.Model).where(entry.Model.uuid == entry_uuid)
        )

    async def update_amount_inside_cajita(
        self,
        new_amount: float,
    ) -> None:
        initial_amount = 2737.39  # 2024-09-10
        amount = new_amount - initial_amount
        if cajita_entry_model := await self.session.scalar(
            statement=select(entry.Model).where(entry.Model.concept == "Cajita")
        ):
            cajita_entry_model.amount = amount
        else:
            self.session.add(
                entry.Model(
                    concept="Cajita",
                    amount=amount,
                    due_date=dt.date.today(),
                    status=entry.Status.CLOSED,
                    frequency=entry.Frequency.ONE_TIME,
                )
            )
