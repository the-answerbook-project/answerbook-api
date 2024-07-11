from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlmodel import Session, select
from starlette import status

from api.dependencies import get_assessment_id, get_session
from api.models.assessment import Assessment
from api.models.student import Student

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
):
    # get username and check to see if they're on the exam as a student or staff

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

    # check auth type
    # auth
    # return success or failure
    return []
