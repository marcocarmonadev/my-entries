from dataclasses import dataclass
from typing import TYPE_CHECKING
from uuid import UUID

from dateutil.relativedelta import relativedelta
from entities import entry

if TYPE_CHECKING:
    from interface_adapters.gateways import entries as entries_gateways
    from interface_adapters.gateways import entry as entry_gateways


@dataclass
class Create:
    entries_database_gateway: "entries_gateways.Database"

    async def as_jsonb(
        self,
        entry_create_schema: entry.CreateSchema,
    ) -> list[entry.ReadSchema]:
        entries = []
        if entry_create_schema.repeat_count == -1:
            if entry_create_schema.repeat_interval is None:
                raise
            entries.append(
                entry.Model(
                    **entry_create_schema.model_dump(
                        exclude={"repeat_count"},
                    ),
                    repeat_forever=True,
                    repeated=False,
                )
            )
        else:
            entries.extend(
                [
                    entry.Model(
                        **entry_create_schema.model_dump(
                            exclude={
                                "repeat_count",
                                "due_date",
                                "repeat_interval",
                            },
                        ),
                        repeat_forever=False,
                        due_date=entry_create_schema.due_date
                        + relativedelta(
                            months=i * entry_create_schema.repeat_interval,
                        ),
                    )
                    for i in range(entry_create_schema.repeat_count + 1)
                ]
            )
        await self.entries_database_gateway.insert(entries)
        return [
            entry.ReadSchema.model_validate(
                _entry,
                from_attributes=True,
            )
            for _entry in entries
        ]


@dataclass
class Update:
    entry_database_gateway: "entry_gateways.Database"

    async def as_jsonb(
        self,
        entry_uuid: UUID,
        entry_update_schema: entry.UpdateSchema,
    ):
        await self.entry_database_gateway.update(
            entry_uuid,
            entry_update_schema,
        )


@dataclass
class Delete:
    entry_database_gateway: "entry_gateways.Database"

    async def as_jsonb(
        self,
        entry_uuid: UUID,
    ):
        await self.entry_database_gateway.delete(entry_uuid)


@dataclass
class Get:
    entry_database_gateway: "entry_gateways.Database"

    async def as_jsonb(
        self,
        entry_uuid: UUID,
    ):
        return entry.ReadSchema.model_validate(
            obj=await self.entry_database_gateway.select_by_uuid(entry_uuid),
            from_attributes=True,
        )


@dataclass
class GetStatistics:
    entries_database_gateway: "entries_gateways.Database"

    async def as_jsonb(self):
        return await self.entries_database_gateway.select_statistics()
