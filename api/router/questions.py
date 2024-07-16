from fastapi import APIRouter, Depends, HTTPException
from starlette.status import HTTP_404_NOT_FOUND

from api.dependencies import get_assessment
from api.schemas.exam import AssessmentSpec, Question

questions_router = APIRouter(prefix="/questions/{question_number}", tags=["exam"])


@questions_router.get(
    "",
    response_model=Question,
    response_model_exclude_unset=True,
    summary="Retrieve exam questions' specification and metadata",
    description="""
Retrieve the specification for the given exam question, including instructions for the question itself, its parts, their sections and tasks.
The response include exam metadata, such as start time and end time for the current user.
""",
)
def get_question(
    question_number: int,
    assessment: AssessmentSpec = Depends(get_assessment),
):
    if question_number not in assessment.questions:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Question not found")
    return assessment.questions[question_number]
