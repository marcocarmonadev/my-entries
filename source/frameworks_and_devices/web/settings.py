from entities import environment
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    ENVIRONMENT: environment.Entity
