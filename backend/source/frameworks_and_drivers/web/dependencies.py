from sqlalchemy.orm import sessionmaker

from source.frameworks_and_drivers.database import session_maker


def _create_session_generator(
    session_maker: sessionmaker,
):
    def generate_session():
        with session_maker.begin() as session:
            yield session

    return generate_session


session_generator = _create_session_generator(session_maker)
