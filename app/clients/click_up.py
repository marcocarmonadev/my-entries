from dataclasses import dataclass
from typing import ClassVar

from httpx import AsyncClient, HTTPStatusError

from core import settings


@dataclass
class Client:
    http_client: AsyncClient

    base_url: ClassVar[str] = "https://api.clickup.com"

    async def create_task_comment(
        self,
        task_id: str,
        comment_text: str,
        *,
        assignee: int | None = None,
        notify_all: bool = False,
    ):
        try:
            response = await self.http_client.post(
                url=f"{self.base_url}/api/v2/task/{task_id}/comment",
                json={
                    "comment_text": comment_text,
                    "assignee": assignee,
                    "notify_all": notify_all,
                },
                headers={
                    "Authorization": settings.CLICKUP_API_KEY,
                },
            )
            response.raise_for_status()
        except HTTPStatusError:
            ...
        else:
            return response.json()

    async def update_task(
        self,
        task_id: str,
        **kwargs,
    ):
        try:
            response = await self.http_client.put(
                url=f"{self.base_url}/api/v2/task/{task_id}",
                json=kwargs,
                headers={
                    "Authorization": settings.CLICKUP_API_KEY,
                },
            )
            response.raise_for_status()
        except HTTPStatusError:
            ...
        else:
            return response.json()

    async def get_task(
        self,
        task_id: str,
        *,
        include_subtasks: bool = False,
        include_markdown_description: bool = False,
    ):
        try:
            response = await self.http_client.get(
                url=f"{self.base_url}/api/v2/task/{task_id}",
                params={
                    "include_subtasks": include_subtasks,
                    "include_markdown_description": include_markdown_description,
                },
                headers={
                    "Authorization": settings.CLICKUP_API_KEY,
                },
            )
            response.raise_for_status()
        except HTTPStatusError:
            ...
        else:
            return response.json()
