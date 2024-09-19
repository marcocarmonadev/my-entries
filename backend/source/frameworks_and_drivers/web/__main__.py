import uvicorn
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DEBUG: bool


def main():
    settings = Settings()  # type: ignore
    uvicorn.run(
        app="source.frameworks_and_drivers.web:app",
        host="127.0.0.1" if settings.DEBUG else "0.0.0.0",
        port=8001 if settings.DEBUG else 8000,
        loop="uvloop",
        reload=settings.DEBUG,
        workers=1 if settings.DEBUG else 4,
        use_colors=settings.DEBUG,
    )


if __name__ == "__main__":
    main()
