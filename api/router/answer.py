from fastapi import APIRouter, Depends
from sqlmodel import Session, asc, select

from api.dependencies import get_assessment_id, get_session
from api.schemas.answer import Answer, AnswerRead

answer_router = APIRouter()


@answer_router.get(
    "/questions/{question_number}/answer",
    tags=["answers"],
    response_model=list[AnswerRead],
    summary="Retrieve answer for question by user",
    description="""
Retrieve the given latest answer by a user including part, section, task.
""",
)
def get_answer(
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
        .order_by(asc(Answer.part), asc(Answer.section), asc(Answer.task))
    )
    return session.exec(query).all()
