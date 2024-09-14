import datetime as dt
from dataclasses import dataclass, field
from typing import Any
from uuid import UUID

import requests

from . import Settings
from .models import Entry, Status


@dataclass
class Client:
    http_session: requests.Session
    settings: Settings = field(
        default_factory=Settings,  # type: ignore
    )

    def create_entry(
        self,
        concept: str,
        amount: float,
        due_date: dt.date,
        status: Status,
        repeat_count: int,
        repeat_interval: int,
    ):
        self.http_session.post(
            url=f"{self.settings.BASE_URL}api/v1/entries",
            json={
                "concept": concept,
                "amount": amount,
                "due_date": due_date.strftime("%Y-%m-%d"),
                "status": status.value,
                "repeat_count": repeat_count,
                "repeat_interval": repeat_interval,
            },
        )

    def get_entries(self):
        response = self.http_session.get(
            url=f"{self.settings.BASE_URL}api/v1/entries",
        )
        return [Entry(**entry) for entry in response.json()]

    def update_entry(
        self,
        entry_uuid: UUID,
        body: dict[str, Any],
    ):
        self.http_session.put(
            url=f"{self.settings.BASE_URL}api/v1/entries/{entry_uuid}",
            json=body,
        )

    def delete_entry(
        self,
        entry_uuid: UUID,
    ):
        self.http_session.delete(
            url=f"{self.settings.BASE_URL}api/v1/entries/{entry_uuid}",
        )

    def delete_entries(
        self,
        entry_uuids: list[UUID],
    ):
        self.http_session.delete(
            url=f"{self.settings.BASE_URL}api/v1/entries",
            json=[str(uuid) for uuid in entry_uuids],
        )

    def get_entries_statistics(self):
        response = self.http_session.get(
            url=f"{self.settings.BASE_URL}api/v1/entries/statistics",
        )
        return response.json()
