from dataclasses import dataclass, field
from typing import Any
from uuid import UUID

import requests

from . import Settings, models


@dataclass
class Client:
    http_session: requests.Session
    settings: Settings = field(
        default_factory=Settings,  # type: ignore
    )

    def create_entry(self, **body):
        try:
            response = self.http_session.post(
                url=f"{self.settings.BASE_URL}api/v1/entries",
                json=body,
            )
            response.raise_for_status()
        except requests.HTTPError as exc:
            raise exc

    def get_entries(self):
        response = self.http_session.get(
            url=f"{self.settings.BASE_URL}api/v1/entries",
        )
        return [models.Entry(**entry) for entry in response.json()]

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

    def update_amount_inside_cajita(
        self,
        new_amount: float,
    ):
        try:
            response = self.http_session.put(
                url=f"{self.settings.BASE_URL}api/v1/entries/amount-inside-cajita",
                json={
                    "new_amount": new_amount,
                },
            )
            response.raise_for_status()
        except requests.HTTPError as exc:
            raise exc

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
