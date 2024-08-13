from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from starlette import status

from api.authentication.jwt_utils import oauth2_scheme
from api.dependencies import (
    get_assessment_spec,
    get_session,
    validate_token,
)
from api.models.student import Student
from api.schemas.exam import AssessmentHeading, AssessmentSpec, Question

exam_router = APIRouter(prefix="/{assessment_code}", tags=["exam"])


@exam_router.get(
    "/summary",
    tags=["exam"],
    response_model=AssessmentHeading,
    summary="Exam summary information",
    description="""
Retrieve the exam summary with user-specific start-time and end-time.
""",
)
def get_summary(
    assessment: AssessmentSpec = Depends(get_assessment_spec),
    _=Depends(validate_token),
):
    return AssessmentHeading(**assessment.model_dump())


@exam_router.get(
    "/questions",
    tags=["exam"],
    response_model=dict[int, Question],
    summary="Exam questions",
    description="Retrieve all the exam questions.",
)
def get_questions(
    assessment: AssessmentSpec = Depends(get_assessment_spec),
    _=Depends(validate_token),
):
    return assessment.questions


@exam_router.get(
    "/students",
    tags=["exam"],
    response_model=list[Student],
    summary="Exam students",
    description="Retrieve all the students enrolled for the exam",
)
def get_students(
    assessment_code: str,
    _=Depends(validate_token),
    session: Session = Depends(get_session),
):
    query = select(Student).where(
        Student.exam_id == assessment_code,
    )
    return session.exec(query).all()
