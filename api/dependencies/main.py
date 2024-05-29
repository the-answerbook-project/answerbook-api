from functools import lru_cache
from typing import Generator

from sqlalchemy.exc import SQLAlchemyError
from sqlmodel import Session

from api.database.connection import engine
from api.settings import Settings


def get_session() -> Generator[Session, None, None]:
    with Session(engine) as s:
        try:
            yield s
            s.commit()
        except SQLAlchemyError as e:
            s.rollback()
            raise e


@lru_cache()
def get_settings() -> Settings:
    return Settings()
