from functools import lru_cache
from typing import Generator

from fastapi import Depends
from sqlalchemy.exc import SQLAlchemyError
from sqlmodel import Session

from api.authentication.ldap_authentication import LdapAuthenticator
from api.database.connection import engine
from api.schemas.exam import Assessment
from api.settings import Settings
from api.yaml_parser import encode_images_in_instructions, parse_yaml


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


def get_assessment_id() -> str:
    return "y2023_12345_exam"


@lru_cache()
def get_ldap_authenticator() -> LdapAuthenticator:
    settings = get_settings()
    return LdapAuthenticator(
        server_url=settings.ldap_server_url, base_dn=settings.ldap_base_dn
    )


def get_assessment(
    settings=Depends(get_settings), assessment_id=Depends(get_assessment_id)
) -> Assessment:
    assessment_dir = settings.assessments_dir / assessment_id
    images_dir = assessment_dir / "images"
    data = parse_yaml(assessment_dir / "assessment.yaml")
    if images_dir.exists():
        data = encode_images_in_instructions(data, images_dir)
    return Assessment(**data)
