from typing import TYPE_CHECKING
from uuid import UUID

from entities import entry, tag
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


@router.post(
    path="",
    responses={
        status.HTTP_200_OK: {
            "model": list[entry.ReadSchema],
        }
    },
)
async def add_entry(
    entry_create_schema: entry.CreateSchema = Body(...),
    session: "AsyncSession" = Depends(
        dependency=database.Session.generate,
    ),
):
    return await entry_controllers.Add(entries_gateways.DatabaseImp(session)).as_jsonb(
        entry_create_schema
    )


@router.patch(
    path="/{entry_uuid}/status",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_204_NO_CONTENT: {
            "model": None,
        }
    },
)
async def update_entry_status(
    entry_uuid: UUID = Path(...),
    entry_update_status_schema: entry.UpdateStatusSchema = Body(...),
    session: "AsyncSession" = Depends(
        dependency=database.Session.generate,
    ),
):
    return await entry_controllers.UpdateStatus(
        entry_gateways.DatabaseImp(session)
    ).as_jsonb(entry_uuid, entry_update_status_schema)


@router.get(
    path="",
    responses={
        status.HTTP_200_OK: {
            "model": list[entry.ReadSchema],
        }
    },
)
async def get_entries(
    session: "AsyncSession" = Depends(
        dependency=database.Session.generate,
    ),
):
    return await entries_controllers.Get(
        entries_gateways.DatabaseImp(session)
    ).as_jsonb()
