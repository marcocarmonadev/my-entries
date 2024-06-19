from pydantic.networks import PostgresDsn
from pydantic_core import MultiHostUrl
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    URL: PostgresDsn = MultiHostUrl(
        "postgresql+asyncpg://postgres:postgres@database:5432/development"
    )
