from fastapi import APIRouter, Depends, HTTPException
from fastapi_jwt import JwtAccessBearerCookie
from pydantic import BaseModel
from sqlmodel import Session, select
from starlette import status
from starlette.responses import JSONResponse

from api.dependencies import get_session, get_settings
from api.models.assessment import Assessment

authentication_router = APIRouter(prefix="/{exam_code}/auth", tags=["exam"])

access_security = JwtAccessBearerCookie(secret_key=get_settings().secret_key)


class Credentials(BaseModel):
    username: str
    password: str


class JwtSubject(BaseModel):
    username: str
    role: str
    exam_code: str


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

    response = JSONResponse(content={"username": credentials.username, "role": role})
    subject = dict(username=credentials.username, role=role, exam_code=exam_code)
    access_token = access_security.create_access_token(subject=subject)
    access_security.set_access_cookie(response, access_token=access_token)
    return response
