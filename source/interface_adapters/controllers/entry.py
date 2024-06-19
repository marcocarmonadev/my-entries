from dataclasses import dataclass
from typing import TYPE_CHECKING
from uuid import UUID

from dateutil.relativedelta import relativedelta
from entities import entry

if TYPE_CHECKING:
    from interface_adapters.gateways import entries as entries_gateways
    from interface_adapters.gateways import entry as entry_gateways


@dataclass
class Add:
    entries_database_gateway: "entries_gateways.Database"

    async def as_jsonb(
        self,
        entry_create_schema: entry.CreateSchema,
    ) -> list[entry.ReadSchema]:
        entry_models = []
        if entry_create_schema.repeat_count == -1:
            if entry_create_schema.repeat_interval is None:
                raise
            entry_models.append(
                entry.Model(
                    **entry_create_schema.model_dump(
                        exclude={"repeat_count"},
                    ),
                    repeat_forever=True,
                    repeated=False,
                )
            )
        else:
            entry_models.extend(
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
        await self.entries_database_gateway.insert(entry_models)
        return [
            entry.ReadSchema.model_validate(
                entry_model,
                from_attributes=True,
            )
            for entry_model in entry_models
        ]


@dataclass
class UpdateStatus:
    entry_database_gateway: "entry_gateways.Database"

    async def as_jsonb(
        self,
        entry_uuid: UUID,
        entry_update_status_schema: entry.UpdateStatusSchema,
    ):
        await self.entry_database_gateway.update_status(
            entry_uuid,
            status=entry_update_status_schema.status,
        )
