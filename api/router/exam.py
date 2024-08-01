from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from starlette import status

from api.dependencies import (
    get_assessment_spec,
    get_session,
)
from api.models.student import Student
from api.schemas.exam import AssessmentSpec, AssessmentSummary, Question

exam_router = APIRouter(prefix="/{assessment_code}", tags=["exam"])


@exam_router.get(
    "/summary",
    tags=["exam"],
    response_model=AssessmentSummary,
    summary="Exam summary information",
    description="""
Retrieve the exam summary with user-specific start-time and end-time.
""",
)
def get_summary(
    assessment: AssessmentSpec | None = Depends(get_assessment_spec),
):
    if assessment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assessment not found.",
        )
    return AssessmentSummary(**assessment.model_dump())


@exam_router.get(
    "/questions",
    tags=["exam"],
    response_model=dict[int, Question],
    summary="Exam questions",
    description="Retrieve all the exam questions.",
)
def get_questions(
    assessment: AssessmentSpec | None = Depends(get_assessment_spec),
):
    if assessment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assessment not found.",
        )
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
    session: Session = Depends(get_session),
):
    query = select(Student).where(
        Student.exam_id == assessment_code,
    )
    return session.exec(query).all()
