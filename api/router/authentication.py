from fastapi import APIRouter, Depends, HTTPException
from fastapi_jwt import JwtAccessBearerCookie
from passlib.context import CryptContext
from pydantic import BaseModel
from sqlmodel import Session, select
from starlette import status
from starlette.responses import JSONResponse

from api.dependencies import get_session, get_settings
from api.models.assessment import Assessment
from api.models.internal_credentials import InternalCredentials

authentication_router = APIRouter(prefix="/{exam_code}/auth", tags=["exam"])

access_security = JwtAccessBearerCookie(secret_key=get_settings().secret_key)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Credentials(BaseModel):
    username: str
    password: str


class JwtSubject(BaseModel):
    username: str
    role: str
    exam_code: str


def get_user_credentials(session, exam_code: str, username: str):
    query = (
        select(InternalCredentials)
        .join(Assessment)
        .where(
            InternalCredentials.username == username, Assessment.exam_code == exam_code
        )
    )
    return session.exec(query).first()


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def internal_authentication(session, exam_code: str, username: str, password: str):
    user_credentials = get_user_credentials(session, exam_code, username)
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


@authentication_router.post(
    "/login",
    summary="Authentication",
    description="""
Login to an assessment
""",
)
def login(
    credentials: Credentials,
    exam_code: str,
    session: Session = Depends(get_session),
):
    query = select(Assessment).where(Assessment.exam_code == exam_code)
    assessment = session.exec(query).first()

    if assessment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assessment not found.",
        )

    role = assessment.get_role(credentials.username)
    if role is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Username not registered for assessment.",
        )
    username, pwd = credentials.username, credentials.password
    internal_authentication(session, exam_code, username, pwd)
    response = JSONResponse(content={"username": username, "role": role})
    subject = dict(username=username, role=role, exam_code=exam_code)
    access_token = access_security.create_access_token(subject=subject)
    access_security.set_access_cookie(response, access_token=access_token)
    return response
