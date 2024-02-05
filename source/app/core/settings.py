from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    CLICKUP_API_KEY: str


settings = Settings()  # type: ignore
