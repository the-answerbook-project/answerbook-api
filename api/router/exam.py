from fastapi import APIRouter, Depends

from api.dependencies import (
    get_assessment_spec,
    validate_token,
)
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
