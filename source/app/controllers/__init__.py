from fastapi.param_functions import Depends
from httpx import AsyncClient

from ..clients import ClickUpClient
from ..core import Dependency
from .click_up import HttpController as ClickUpHttpController


class Factory:
    @staticmethod
    def create_click_up_http_controller(
        http_client: AsyncClient = Depends(
            dependency=Dependency.generate_http_client,
        ),
    ):
        return ClickUpHttpController(ClickUpClient(http_client))
