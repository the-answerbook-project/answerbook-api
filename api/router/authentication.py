from datetime import datetime, timedelta, timezone

import jwt
from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from sqlmodel import Session
from starlette import status

from api.authentication.internal_authentication import (
    get_user_credentials,
    verify_password,
)
from api.authentication.ldap_authentication import LdapAuthenticator
from api.dependencies import (
    get_assessment_config,
    get_assessment_spec,
    get_ldap_authenticator,
    get_session,
    get_settings,
)
from api.models.assessment import Assessment, AuthenticationMode
from api.models.revoked_token import RevokedToken
from api.schemas.exam import AssessmentSpec

authentication_router = APIRouter(
    prefix="/{assessment_code}/auth", tags=["authentication"]
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

JWT_ALGO = "HS256"
TWO_HOURS_IN_MINUTES = 120


class JwtSubject(BaseModel):
    username: str
    role: str
    assessment_code: str


class Token(BaseModel):
    access_token: str
    token_type: str


def create_access_token(subject: dict, expires_delta: timedelta):
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode = {"sub": subject.copy(), "exp": expire}
    encoded_jwt = jwt.encode(to_encode, get_settings().secret_key, algorithm=JWT_ALGO)
    return encoded_jwt


def authenticate_via_internal_creds_match(
    session, assessment_code: str, username: str, password: str
):
    user_credentials = get_user_credentials(session, assessment_code, username)
    if not user_credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User credentials not found for the given username.",
        )
    if not verify_password(password, user_credentials.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials.",
        )


def authenticate_via_ldap(
    ldap_authenticator: LdapAuthenticator, username: str, password: str
):
    if not ldap_authenticator.authenticate(username, password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials.",
        )


def calculate_token_expiration(
    assessment_duration: int, extensions: dict[str, str]
) -> timedelta:
    max_extension = max(*extensions.values(), "0")
    max_extension = max_extension.split(" ")[0].replace("minutes", "")
    minutes = assessment_duration
    minutes += int(max_extension)
    minutes += TWO_HOURS_IN_MINUTES
    return timedelta(minutes=minutes)


@authentication_router.post(
    "/login",
    summary="Assessment authentication",
    description="""
Log in to the assessment. The provided credentials are checked against the configured authentication method.
Possible authentication methods are
- **INTERNAL** to verify the provided creds against those generated and stored per exam
- **LDAP** to verify the provided creds against those available in the indicated LDAP server
""",
)
def login(
    assessment_code: str,
    credentials: OAuth2PasswordRequestForm = Depends(),
    ldap_authenticator: LdapAuthenticator = Depends(get_ldap_authenticator),
    config: Assessment | None = Depends(get_assessment_config),
    spec: AssessmentSpec | None = Depends(get_assessment_spec),
    session: Session = Depends(get_session),
) -> Token:
    if config is None or spec is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assessment not found.",
        )

    role = config.get_role(credentials.username)
    if role is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Username not registered for assessment.",
        )
    username, pwd = credentials.username, credentials.password

    match config.authentication_mode:
        case AuthenticationMode.LDAP:
            authenticate_via_ldap(ldap_authenticator, username, pwd)
        case AuthenticationMode.INTERNAL:
            authenticate_via_internal_creds_match(
                session, assessment_code, username, pwd
            )

    subject = dict(username=username, role=role, assessment_code=assessment_code)
    access_token_expires = calculate_token_expiration(spec.duration, spec.extensions)
    access_token = create_access_token(
        subject=subject, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


@authentication_router.delete("/logout")
async def logout(
    assessment_code: str,
    token: str = Depends(oauth2_scheme),
    session: Session = Depends(get_session),
):
    try:
        payload = jwt.decode(token, get_settings().secret_key, algorithms=[JWT_ALGO])
        expiration = datetime.fromtimestamp(payload["exp"], tz=timezone.utc)
    except jwt.ExpiredSignatureError:
        expiration = datetime.now(timezone.utc)
    revoked_token = RevokedToken(token=token, expiration=expiration)
    session.add(revoked_token)
    session.commit()
    return Response(status_code=204)
