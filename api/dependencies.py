from functools import lru_cache
from typing import Generator

import jwt
from fastapi import Depends, HTTPException
from jwt import InvalidTokenError
from sqlalchemy import exists
from sqlalchemy.exc import SQLAlchemyError
from sqlmodel import Session, select
from starlette import status

from api.authentication.jwt_utils import JWT_ALGO, JwtSubject, oauth2_scheme
from api.authentication.ldap_authentication import LdapAuthenticator
from api.database.connection import engine
from api.models.assessment import Assessment, UserRole
from api.models.student import Marker, Student
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
) -> AssessmentSpec:
    assessment_dir = settings.assessments_dir / assessment_code
    images_dir = assessment_dir / "images"
    yaml_file = assessment_dir / "assessment.yaml"

    if not yaml_file.exists():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assessment not found.",
        )

    data = parse_yaml(yaml_file)
    if images_dir.exists():
        data = encode_images_in_instructions(data, images_dir)
    return AssessmentSpec(**data)


def get_assessment_config(
    assessment_code: str, session: Session = Depends(get_session)
) -> Assessment:
    query = select(Assessment).where(Assessment.code == assessment_code)
    if config := session.exec(query).first():
        return config
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Assessment not found.",
    )


def validate_token(
    token=Depends(oauth2_scheme),
    session: Session = Depends(get_session),
    settings: Settings = Depends(get_settings),
    assessment=Depends(get_assessment_config),
) -> JwtSubject:
    """
    We extract the token subject after validation.
    Validation of the token consists of checking for
    - assessment_code consistency between the code in the sub and the code in the path param
    - username consistency with the assessment according to the role specified in the sub
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid token.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[JWT_ALGO])
        raw_subject = payload.get("sub")
        if raw_subject is None:
            raise credentials_exception
        subject = JwtSubject(**raw_subject)
        if subject.assessment_code != assessment.code:
            raise credentials_exception
        model: type[Student | Marker] = (
            Student if subject.role == UserRole.CANDIDATE else Marker
        )
        stmt = exists().where(
            model.username == subject.username,  # type: ignore
            model.assessment_id == assessment.id,
        )
        if not session.query(stmt).scalar():
            raise credentials_exception
        return subject
    except InvalidTokenError:
        raise credentials_exception


def verify_user_is_marker(sub: JwtSubject = Depends(validate_token)) -> str:
    if sub.role != UserRole.MARKER:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permissions to access this resource.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return sub.username
