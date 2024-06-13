from fastapi import APIRouter, Depends

from api.dependencies import get_assessment
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
