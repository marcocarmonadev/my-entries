from alembic import command
from alembic.config import Config


def main():
    command.upgrade(
        config=Config("alembic.ini"),
        revision="head",
    )


if __name__ == "__main__":
    main()
