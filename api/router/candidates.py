from fastapi import APIRouter, Depends

from api.authentication.jwt_utils import JwtSubject
from api.dependencies import get_assessment_spec, validate_token
from api.schemas.exam import AssessmentSpec, AssessmentSummary
from api.utils import parse_extension

candidates_router = APIRouter(
    prefix="/{assessment_code}/candidates/me", tags=["candidates"]
)


@candidates_router.get(
    "/exam-summary",
    response_model=AssessmentSummary,
    summary="Exam summary information",
    description="Retrieve the exam summary with candidate-specific start-time and end-time.",
)
def get_exam_summary(
    assessment: AssessmentSpec = Depends(get_assessment_spec),
    sub: JwtSubject = Depends(validate_token),
):
    assessment.duration += parse_extension(assessment.extensions.get(sub.username, "0"))
    return AssessmentSummary(**assessment.model_dump())
