from typing import TYPE_CHECKING, ClassVar

import uvicorn

from .settings import get_settings
from .types import Environment

if TYPE_CHECKING:
    from . import Settings


class Server:
    settings: ClassVar["Settings"] = get_settings()

    @staticmethod
    def create() -> None:
        is_development = Server.settings.ENVIRONMENT != Environment.PRODUCTION
        uvicorn.run(
            app="routers:API.create",
            host="0.0.0.0",
            loop="uvloop",
            port=8001 if is_development else 8000,
            reload=is_development,
            workers=4,
            use_colors=is_development,
            factory=True,
        )
