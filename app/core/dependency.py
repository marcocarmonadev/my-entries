from dataclasses import dataclass
from typing import AsyncGenerator

from httpx import AsyncClient


@dataclass
class Dependency:
    @staticmethod
    async def generate_http_client() -> AsyncGenerator[AsyncClient, None]:
        async with AsyncClient(
            timeout=None,
        ) as http_client:
            yield http_client
