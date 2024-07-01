from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from api.dependencies import get_assessment, get_assessment_id, get_session
from api.models.student import Student
from api.schemas.exam import Assessment, AssessmentSummary, Question

exam_router = APIRouter(tags=["exam"])


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
    assessment: Assessment = Depends(get_assessment),
):
    return AssessmentSummary(**assessment.dict())


@exam_router.get(
    "/questions",
    tags=["exam"],
    response_model=dict[int, Question],
    summary="Exam questions",
    description="Retrieve all the exam questions.",
)
def get_questions(
    assessment: Assessment = Depends(get_assessment),
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
    assessment_id: str = Depends(get_assessment_id),
    session: Session = Depends(get_session),
):
    query = select(Student).where(
        Student.exam_id == assessment_id,
    )
    return session.exec(query).all()
