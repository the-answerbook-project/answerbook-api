from fastapi import APIRouter, Depends, HTTPException
from starlette.status import HTTP_404_NOT_FOUND

from api.dependencies import get_assessment
from api.schemas.exam import Assessment, AssessmentSummary, Question

exam_router = APIRouter()


@exam_router.get(
    "/questions/{question_number}",
    tags=["exam"],
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
    assessment: Assessment = Depends(get_assessment),
):
    if question_number not in assessment.questions:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Question not found")
    return assessment.questions[question_number]

# ------------------------------------------ Answers



@exam_router.get(
    "/questions/{question_number}/answer",
    tags=["exam"],
    summary="Retrieve answer for question by user",
    description="""
Retrieve the given latest answer by a user including part, section, task.
""",
)
def get_answer(
    question_number: int,
    # assessment: Assessment = Depends(get_assessment),
):
    return "answer"


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
