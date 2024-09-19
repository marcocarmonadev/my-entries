import sys

from pydantic_settings import BaseSettings
from streamlit.web import cli as streamlit_cli


class Settings(BaseSettings):
    DEBUG: bool = False


def main():
    settings = Settings()
    sys.argv = [
        "streamlit",
        "run",
        "source/frameworks_and_drivers/user_interface/__init__.py",
    ]

    if settings.DEBUG:
        sys.argv += [
            "--server.port",
            "8502",
            "--server.runOnSave",
            "true",
        ]
    streamlit_cli.main()


if __name__ == "__main__":
    main()
