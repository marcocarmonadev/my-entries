from pydantic.networks import HttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="TURSO_",
    )

    DATABASE_URL: HttpUrl
    AUTH_TOKEN: str | None = None


def get_url(
    settings: Settings,
):
    url = f"sqlite+{settings.DATABASE_URL}/"
    if settings.AUTH_TOKEN:
        url += f"?authToken={settings.AUTH_TOKEN}&secure=true"
    print(url)
    return url


def _create_engine(
    settings: Settings,
):
    url = get_url(settings)
    is_development_mode = False
    if settings.AUTH_TOKEN:
        is_development_mode = True
    return create_engine(
        url,
        echo=is_development_mode,
        connect_args={
            "check_same_thread": False,
        },
    )


session_maker = sessionmaker(
    bind=_create_engine(
        settings=Settings(),  # type: ignore
    ),
    expire_on_commit=True,
)
