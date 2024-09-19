from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="DATABASE_",
    )

    URL: str
    DEBUG: bool


def _create_engine(
    settings: Settings,
):
    return create_engine(
        url=settings.URL,
        echo=settings.DEBUG,
        connect_args={
            "check_same_thread": False,
        },
        isolation_level="AUTOCOMMIT",
    )


session_maker = sessionmaker(
    bind=_create_engine(
        settings=Settings(),  # type: ignore
    ),
    expire_on_commit=True,
)
