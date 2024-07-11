from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlmodel import Session, select

from api.dependencies import get_session

authentication_router = APIRouter(prefix="/{exam_code}/auth", tags=["exam"])


class Credentials(BaseModel):
    username: str
    password: str


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
    # assessment_id: str = Depends(get_assessment_id),
):
    return []


@authentication_router.delete(
    "/logout",
    summary="Authentication",
    description="""
Login to an assessment
""",
)
def logout(
    exam_code: str,
    session: Session = Depends(get_session),
    # assessment_id: str = Depends(get_assessment_id),
):
    return []
