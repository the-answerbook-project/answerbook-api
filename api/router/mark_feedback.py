from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from api.dependencies import get_assessment_id, get_session
from api.schemas.mark_feedback import (
    MarkFeedback,
    MarkFeedbackHistory,
    MarkFeedbackRead,
)

mark_feedback_router = APIRouter(
    prefix="/questions/{question_number}", tags=["marking"]
)


@mark_feedback_router.get(
    "/mark",
    response_model=list[MarkFeedbackRead],
    summary="Retrieve user marks and feedback for question",
    description="""
Retrieve the latest (and historical) marks for answers to a question by user
""",
)
def get_marks_feedback_for_question_number(
    question_number: int,
    session: Session = Depends(get_session),
    assessment_id: str = Depends(get_assessment_id),
):
    query = (
        select(MarkFeedback)
        .where(
            MarkFeedback.question == question_number,
            MarkFeedback.exam_id == assessment_id,
            MarkFeedback.username == "hpotter",
        )
        .order_by(MarkFeedback.part, MarkFeedback.section, MarkFeedback.task)  # type: ignore
    )
    return session.exec(query).all()
