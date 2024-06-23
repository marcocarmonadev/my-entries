from abc import ABC, abstractmethod
from dataclasses import dataclass
from uuid import UUID

from entities import entries, entry
from sqlalchemy.dialects import postgresql
from sqlalchemy.engine.result import ScalarResult
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import and_, delete, func, select


class Database(ABC):
    @abstractmethod
    async def insert(
        self,
        entry_models: list[entry.Model],
    ) -> None: ...

    @abstractmethod
    async def select(self) -> ScalarResult[entry.Model]: ...

    @abstractmethod
    async def select_actives(self) -> ScalarResult[entry.Model]: ...

    @abstractmethod
    async def delete(
        self,
        entry_uuids: list[UUID],
    ) -> None: ...

    @abstractmethod
    async def select_statistics(self) -> entries.StatisticsSchema: ...


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

    async def select_actives(self) -> ScalarResult[entry.Model]:
        return await self.session.scalars(
            statement=select(entry.Model)
            .where(entry.Model.status != entry.Status.CLOSED)
            .order_by(entry.Model.due_date),
        )

    async def delete(
        self,
        entry_uuids: list[UUID],
    ):
        await self.session.execute(
            statement=delete(entry.Model).where(entry.Model.uuid.in_(entry_uuids))
        )

    async def select_statistics(self) -> entries.StatisticsSchema:
        if not (
            row := (
                await self.session.execute(
                    statement=select(
                        func.sum(
                            entry.Model.amount,
                        )
                        .cast(
                            type_=postgresql.NUMERIC,
                        )
                        .label(
                            name="total_amount",
                        ),
                        func.sum(
                            entry.Model.amount,
                        )
                        .filter(entry.Model.amount >= 0)
                        .cast(
                            type_=postgresql.NUMERIC,
                        )
                        .label(
                            name="income_amount",
                        ),
                        func.sum(
                            entry.Model.amount,
                        )
                        .filter(entry.Model.amount < 0)
                        .cast(
                            type_=postgresql.NUMERIC,
                        )
                        .label(
                            name="expense_amount",
                        ),
                        func.sum(
                            entry.Model.amount,
                        )
                        .filter(
                            and_(
                                entry.Model.amount < 0,
                                entry.Model.status == entry.Status.COMPLETED,
                            )
                        )
                        .cast(
                            type_=postgresql.NUMERIC,
                        )
                        .label(
                            name="complete_expense_amount",
                        ),
                    ).where(entry.Model.status != entry.Status.PENDING)
                )
            ).fetchone()
        ):
            raise
        total_amount, income_amount, expense_amount, complete_expense_amount = row
        return entries.StatisticsSchema(
            total_amount=total_amount or 0,
            income_amount=income_amount or 0,
            expense_amount=expense_amount or 0,
            complete_expense_amount=complete_expense_amount or 0,
        )
