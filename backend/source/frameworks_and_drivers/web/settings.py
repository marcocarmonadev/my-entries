from pydantic_settings import BaseSettings

from source.entities import environment


class Settings(BaseSettings):
    ENVIRONMENT: environment.Entity
