from functools import lru_cache
from typing import Generator

from fastapi import Depends
from sqlalchemy.exc import SQLAlchemyError
from sqlmodel import Session, select

from api.authentication.ldap_authentication import LdapAuthenticator
from api.database.connection import engine
from api.models.assessment import Assessment
from api.schemas.exam import AssessmentSpec
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


def get_assessment_spec(
    assessment_code: str, settings: Settings = Depends(get_settings)
) -> AssessmentSpec | None:
    assessment_dir = settings.assessments_dir / assessment_code
    images_dir = assessment_dir / "images"
    yaml_file = assessment_dir / "assessment.yaml"

    if not yaml_file.exists():
        return None

    data = parse_yaml(yaml_file)
    if images_dir.exists():
        data = encode_images_in_instructions(data, images_dir)
    return AssessmentSpec(**data)


def get_assessment_config(
    assessment_code: str, session: Session = Depends(get_session)
) -> Assessment | None:
    query = select(Assessment).where(Assessment.code == assessment_code)
    return session.exec(query).first()
