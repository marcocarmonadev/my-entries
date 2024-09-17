from typing import TYPE_CHECKING
from uuid import UUID

from fastapi import Query
from fastapi.param_functions import Body, Depends, Path
from fastapi.routing import APIRouter
from starlette import status

from source.entities import entries, entry
from source.frameworks_and_drivers.web.dependencies import session_generator
from source.frameworks_and_drivers.web.enums import Tag
from source.interface_adapters.controllers import entries as entries_controllers
from source.interface_adapters.controllers import entry as entry_controllers
from source.interface_adapters.gateways import entries as entries_gateways
from source.interface_adapters.gateways import entry as entry_gateways

if TYPE_CHECKING:
    from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/entries",
    tags=[
        Tag.ENTRIES,
    ],
)


@router.delete(
    path="/{entry_uuid}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_entry(
    entry_uuid: UUID = Path(...),
    session: "Session" = Depends(
        dependency=session_generator,
    ),
):
    entry_controllers.Delete(
        entry_database_gateway=entry_gateways.DatabaseImp(session),
    ).as_jsonb(entry_uuid)


@router.delete(
    path="",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_entries(
    entry_uuids: list[UUID] = Body(...),
    session: "Session" = Depends(
        dependency=session_generator,
    ),
):
    entries_controllers.Delete(
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
def get_entries(
    only_active: bool = Query(
        default=True,
    ),
    session: "Session" = Depends(
        dependency=session_generator,
    ),
):
    return entries_controllers.Get(
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
def get_entries_statistics(
    session: "Session" = Depends(
        dependency=session_generator,
    ),
):
    return entries_controllers.GetStatistics(
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
def get_entry(
    entry_uuid: UUID = Path(...),
    session: "Session" = Depends(
        dependency=session_generator,
    ),
):
    return entry_controllers.Get(
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
def create_entry(
    entry_create_schema: entry.CreateSchema = Body(...),
    session: "Session" = Depends(
        dependency=session_generator,
    ),
):
    return entry_controllers.Create(
        entries_database_gateway=entries_gateways.DatabaseImp(session),
    ).as_jsonb(entry_create_schema)


@router.put(
    path="/amount-inside-cajita",
    status_code=status.HTTP_204_NO_CONTENT,
)
def update_amount_inside_cajita(
    body: entry.UpdateAmountInsideCajita,
    session: "Session" = Depends(
        dependency=session_generator,
    ),
):
    entry_controllers.UpdateAmountInsideCajita(
        entry_database_gateway=entry_gateways.DatabaseImp(session),
    ).as_jsonb(
        new_amount=body.new_amount,
    )


@router.put(
    path="/{entry_uuid}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def update_entry(
    entry_uuid: UUID = Path(...),
    entry_update_schema: entry.UpdateSchema = Body(...),
    session: "Session" = Depends(
        dependency=session_generator,
    ),
):
    entry_controllers.Update(
        entry_database_gateway=entry_gateways.DatabaseImp(session),
    ).as_jsonb(entry_uuid, entry_update_schema)
