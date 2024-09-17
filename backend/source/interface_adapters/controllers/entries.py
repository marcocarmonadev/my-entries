from dataclasses import dataclass
from typing import TYPE_CHECKING
from uuid import UUID

from source.entities import entry

if TYPE_CHECKING:
    from source.interface_adapters.gateways import entries as entries_gateways


@dataclass
class Get:
    entries_database_gateway: "entries_gateways.Database"

    def as_jsonb(
        self,
        only_active: bool,
    ) -> list[entry.ReadSchema]:
        if only_active:
            select_function = self.entries_database_gateway.select_actives()
        else:
            select_function = self.entries_database_gateway.select()
        return [
            entry.ReadSchema.model_validate(
                _entry,
                from_attributes=True,
            )
            for _entry in select_function
        ]


@dataclass
class GetStatistics:
    entries_database_gateway: "entries_gateways.Database"

<<<<<<< HEAD:source/interface_adapters/controllers/entries.py
    async def as_jsonb(self):
        return await self.entries_database_gateway.select_statistics()
=======
    def as_jsonb(self):
        return self.entries_database_gateway.select_statistics()
>>>>>>> development:backend/source/interface_adapters/controllers/entries.py


@dataclass
class Delete:
    entries_database_gateway: "entries_gateways.Database"

    def as_jsonb(
        self,
        uuids: list[UUID],
    ) -> None:
        self.entries_database_gateway.delete(uuids)
