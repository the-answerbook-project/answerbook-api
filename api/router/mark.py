from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from api.dependencies import get_assessment_id, get_session
from api.schemas.answer import Answer, AnswerRead
from api.schemas.mark import (
    Mark,
    MarkRead,
)

marking_router = APIRouter(prefix="/{student_username}", tags=["marking"])


@marking_router.get(
    "/marks",
    response_model=list[MarkRead],
    summary="Retrieve user marks and feedback for exam questions",
    description="""
Retrieve the latest (and historical) marks for answers to a question by user
""",
)
def get_marks_for_question(
    student_username: str,
    session: Session = Depends(get_session),
    assessment_id: str = Depends(get_assessment_id),
):
    query = (
        select(Mark)
        .where(
            Mark.exam_id == assessment_id,
            Mark.username == student_username,
        )
        .order_by(Mark.question, Mark.part, Mark.section)  # type: ignore
    )
    return session.exec(query).all()


@marking_router.get(
    "/answers",
    response_model=list[AnswerRead],
    summary="Retrieve student answers for all questions in exam",
    description="""
Retrieve the latest answers for all questions in exam
""",
)
def get_answers_for_student(
    student_username: str,
    session: Session = Depends(get_session),
    assessment_id: str = Depends(get_assessment_id),
):
    query = (
        select(Answer)
        .where(
            Answer.exam_id == assessment_id,
            Answer.username == student_username,
        )
        .order_by(Answer.question, Answer.part, Answer.section, Answer.task)  # type: ignore
    )
    return session.exec(query).all()
