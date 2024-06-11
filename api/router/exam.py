from fastapi import APIRouter, Depends

from api.dependencies import get_assessment
from api.schemas.exam import Assessment, AssessmentSummary

exam_router = APIRouter(tags=["exam"])


@exam_router.get(
    "/summary",
    tags=["exam"],
    response_model=AssessmentSummary,
    summary="Retrieve exam summary information",
    description="""
Retrieve the exam summary with user-specific start-time and end-time.
""",
)
def get_summary(
    assessment: Assessment = Depends(get_assessment),
):
    return AssessmentSummary(**assessment.dict())
