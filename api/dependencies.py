from functools import lru_cache
from typing import Generator

from fastapi import Depends
from sqlalchemy.exc import SQLAlchemyError
from sqlmodel import Session

from api.database.connection import engine
from api.schemas.exam import Assessment
from api.settings import Settings
from api.yaml_parser import parse_yaml


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


def get_assessment_config_file() -> str:
    return "y2023_12345_exam.yaml"


def get_assessment(
    settings=Depends(get_settings), config_file=Depends(get_assessment_config_file)
) -> Assessment:
    return Assessment(**parse_yaml(settings.assessments_dir / config_file))
