from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from api.dependencies import get_assessment_id, get_session
from api.schemas.mark_feedback import (
    MarkFeedback,
    MarkFeedbackRead,
)

mark_feedback_router = APIRouter(prefix="/marks", tags=["marking"])


@mark_feedback_router.get(
    "/{student_username}",
    response_model=list[MarkFeedbackRead],
    summary="Retrieve user marks and feedback for question",
    description="""
Retrieve the latest (and historical) marks for answers to a question by user
""",
)
def get_marks_feedback_for_question_number(
    # question_number: int,
    student_username: str,
    session: Session = Depends(get_session),
    assessment_id: str = Depends(get_assessment_id),
):
    query = (
        select(MarkFeedback)
        .where(
            MarkFeedback.exam_id == assessment_id,
            MarkFeedback.username == student_username,
        )
        .order_by(
            MarkFeedback.question,  # type: ignore
            MarkFeedback.part,  # type: ignore
            MarkFeedback.section,  # type: ignore
            MarkFeedback.task,  # type: ignore
        )  # type: ignore
    )
    return session.exec(query).all()
