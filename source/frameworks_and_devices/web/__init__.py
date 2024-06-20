from dataclasses import dataclass
from typing import ClassVar

import uvicorn
from entities import environment

from .settings import Settings


@dataclass
class Server:
    _settings: ClassVar[Settings] = Settings()  # type: ignore
    _is_development_mode: ClassVar[bool] = _settings.ENVIRONMENT == environment.Entity.DEVELOPMENT

    @classmethod
    def run(cls):
        uvicorn.run(
            app="frameworks_and_devices.web.api:build",
            host="0.0.0.0",
            port=8001 if cls._is_development_mode else 8000,
            loop="uvloop",
            reload=cls._is_development_mode,
            workers=None if cls._is_development_mode else 4,
            use_colors=cls._is_development_mode,
            factory=True,
            reload_dirs=[
                "source",
            ],
        )
