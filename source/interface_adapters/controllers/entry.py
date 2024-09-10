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
        match entry_create_schema.frequency:
            case entry.Frequency.ONE_TIME:
                entries.append(
                    entry.Model(
                        **entry_create_schema.model_dump(
                            exclude={
                                "repeat_interval",
                                "repeat_count",
                            }
                        )
                    )
                )
            case entry.Frequency.BI_WEEKLY:
                if entry_create_schema.repeat_count == 0:
                    entries.append(
                        entry.Model(
                            **entry_create_schema.model_dump(
                                exclude={
                                    "repeat_interval",
                                    "repeat_count",
                                    "due_date",
                                }
                            ),
                            due_date=entry.get_nearest_fortnight_date(
                                entry_create_schema.due_date
                            ),
                            repeat_forever=True,
                        )
                    )
                else:
                    entry_model_data = entry_create_schema.model_dump(
                        exclude={
                            "repeat_interval",
                            "repeat_count",
                            "due_date",
                        },
                    )

                    nearest_fortnight_date = entry.get_nearest_fortnight_date(
                        entry_create_schema.due_date
                    )
                    due_dates = []
                    for i in range(entry_create_schema.repeat_count):
                        if i != 0:
                            nearest_fortnight_date = (
                                entry.get_next_nearest_fortnight_date(
                                    nearest_fortnight_date
                                )
                            )
                        due_dates.append(nearest_fortnight_date)
                    entries.extend(
                        [
                            entry.Model(
                                **entry_model_data,
                                due_date=due_date,
                            )
                            for due_date in due_dates
                        ]
                    )
            case another_frequency:
                if entry_create_schema.repeat_count == 0:
                    entries.append(
                        entry.Model(
                            **entry_create_schema.model_dump(
                                exclude={
                                    "repeat_count",
                                }
                            ),
                            repeat_forever=True,
                        )
                    )
                else:
                    match another_frequency:
                        case entry.Frequency.WEEKLY:
                            delta = "weeks"
                        case entry.Frequency.MONTLY:
                            delta = "months"
                        case entry.Frequency.YEARLY:
                            delta = "years"

                    entry_model_data = entry_create_schema.model_dump(
                        exclude={
                            "repeat_interval",
                            "repeat_count",
                            "due_date",
                        },
                    )

                    entries.extend(
                        [
                            entry.Model(
                                **entry_model_data,
                                due_date=entry_create_schema.due_date
                                + relativedelta(
                                    **kwargs,  # type: ignore
                                ),
                            )
                            for kwargs in [
                                {delta: i * entry_create_schema.repeat_interval}
                                for i in range(entry_create_schema.repeat_count)
                            ]
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
class UpdateAmountInsideCajita:
    entry_database_gateway: "entry_gateways.Database"

    async def as_jsonb(
        self,
        new_amount: float,
    ):
        await self.entry_database_gateway.update_amount_inside_cajita(new_amount)
