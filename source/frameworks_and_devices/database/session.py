from dataclasses import dataclass
from typing import ClassVar

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from . import Settings


@dataclass
class Session:
    _settings: ClassVar[Settings] = Settings()
    _url = _settings.URL.unicode_string()
    _is_development_environment: ClassVar[bool] = (
        _settings.URL.unicode_string().endswith("development")
    )
    _engine: ClassVar[AsyncEngine] = create_async_engine(
        _url,
        echo=_is_development_environment,
        echo_pool="debug" if _is_development_environment else False,
        pool_size=20,
    )
    _maker: ClassVar[async_sessionmaker[AsyncSession]] = async_sessionmaker(
        bind=_engine,
        expire_on_commit=True,
    )

    @classmethod
    async def generate(cls):
        async with cls._maker.begin() as session:
            yield session
