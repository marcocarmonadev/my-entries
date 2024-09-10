from typing import TYPE_CHECKING
from uuid import UUID

from entities import entries, entry, tag
from fastapi import Query
from fastapi.param_functions import Body, Depends, Path
from fastapi.routing import APIRouter
from frameworks_and_devices import database
from interface_adapters.controllers import entries as entries_controllers
from interface_adapters.controllers import entry as entry_controllers
from interface_adapters.gateways import entries as entries_gateways
from interface_adapters.gateways import entry as entry_gateways
from starlette import status

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(
    prefix="/entries",
    tags=[
        tag.Entity.ENTRIES,
    ],
)


@router.delete(
    path="/{entry_uuid}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_entry(
    entry_uuid: UUID = Path(...),
    session: "AsyncSession" = Depends(
        dependency=database.Session.generate,
    ),
):
    await entry_controllers.Delete(
        entry_database_gateway=entry_gateways.DatabaseImp(session),
    ).as_jsonb(entry_uuid)


@router.delete(
    path="",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_entries(
    entry_uuids: list[UUID] = Body(...),
    session: "AsyncSession" = Depends(
        dependency=database.Session.generate,
    ),
):
    await entries_controllers.Delete(
        entries_database_gateway=entries_gateways.DatabaseImp(session),
    ).as_jsonb(entry_uuids)


@router.get(
    path="",
    responses={
        status.HTTP_200_OK: {
            "model": list[entry.ReadSchema],
        }
    },
)
async def get_entries(
    only_active: bool = Query(
        default=True,
    ),
    session: "AsyncSession" = Depends(
        dependency=database.Session.generate,
    ),
):
    return await entries_controllers.Get(
        entries_database_gateway=entries_gateways.DatabaseImp(session),
    ).as_jsonb(only_active)


@router.get(
    path="/statistics",
    responses={
        status.HTTP_200_OK: {
            "model": entries.StatisticsSchema,
        }
    },
)
async def get_entries_statistics(
    session: "AsyncSession" = Depends(
        dependency=database.Session.generate,
    ),
):
    return await entries_controllers.GetStatistics(
        entries_database_gateway=entries_gateways.DatabaseImp(session),
    ).as_jsonb()


@router.get(
    path="/{entry_uuid}",
    responses={
        status.HTTP_200_OK: {
            "model": entry.ReadSchema,
        }
    },
)
async def get_entry(
    entry_uuid: UUID = Path(...),
    session: "AsyncSession" = Depends(
        dependency=database.Session.generate,
    ),
):
    return await entry_controllers.Get(
        entry_database_gateway=entry_gateways.DatabaseImp(session),
    ).as_jsonb(entry_uuid)


@router.post(
    path="",
    responses={
        status.HTTP_201_CREATED: {
            "model": list[entry.ReadSchema],
        }
    },
)
async def create_entry(
    entry_create_schema: entry.CreateSchema = Body(...),
    session: "AsyncSession" = Depends(
        dependency=database.Session.generate,
    ),
):
    return await entry_controllers.Create(
        entries_database_gateway=entries_gateways.DatabaseImp(session),
    ).as_jsonb(entry_create_schema)


@router.put(
    path="/amount-inside-cajita",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def update_amount_inside_cajita(
    body: entry.UpdateAmountInsideCajita,
    session: "AsyncSession" = Depends(
        dependency=database.Session.generate,
    ),
):
    await entry_controllers.UpdateAmountInsideCajita(
        entry_database_gateway=entry_gateways.DatabaseImp(session),
    ).as_jsonb(
        new_amount=body.new_amount,
    )


@router.put(
    path="/{entry_uuid}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def update_entry(
    entry_uuid: UUID = Path(...),
    entry_update_schema: entry.UpdateSchema = Body(...),
    session: "AsyncSession" = Depends(
        dependency=database.Session.generate,
    ),
):
    await entry_controllers.Update(
        entry_database_gateway=entry_gateways.DatabaseImp(session),
    ).as_jsonb(entry_uuid, entry_update_schema)
