from dataclasses import dataclass
from typing import TYPE_CHECKING

from entities import entry

if TYPE_CHECKING:
    from interface_adapters.gateways import entries as entries_gateways


@dataclass
class Get:
    entries_database_gateway: "entries_gateways.Database"

    async def as_jsonb(self) -> list[entry.ReadSchema]:
        return [
            entry.ReadSchema.model_validate(
                entry_model,
                from_attributes=True,
            )
            for entry_model in await self.entries_database_gateway.select()
        ]
