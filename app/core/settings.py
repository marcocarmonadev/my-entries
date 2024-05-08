from pydantic_settings import BaseSettings
from functools import lru_cache
from .types import Environment


class Settings(BaseSettings):
    CLICKUP_API_KEY: str
    ENVIRONMENT: Environment


settings = Settings()  # type: ignore


@lru_cache
def get_settings() -> Settings:
    return Settings()  # type:ignore
