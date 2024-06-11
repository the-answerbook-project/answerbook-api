from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from starlette.status import HTTP_404_NOT_FOUND

from api.dependencies import get_assessment, get_assessment_id, get_session
from api.schemas.answer import Answer, AnswerRead
from api.schemas.exam import Assessment, Question

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
    assessment: Assessment = Depends(get_assessment),
):
    if question_number not in assessment.questions:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Question not found")
    return assessment.questions[question_number]


@questions_router.get(
    "/answer",
    response_model=list[AnswerRead],
    summary="Retrieve user answer to question",
    description="""
Retrieve the latest user answer to the given question's tasks.
""",
)
def get_answer_to_question(
    question_number: int,
    session: Session = Depends(get_session),
    assessment_id: str = Depends(get_assessment_id),
):
    query = (
        select(Answer)
        .where(
            Answer.question == question_number,
            Answer.exam_id == assessment_id,
            Answer.username == "hpotter",
        )
        .order_by(Answer.part, Answer.section, Answer.task)  # type: ignore
    )
    return session.exec(query).all()
