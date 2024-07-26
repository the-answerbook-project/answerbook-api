from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from starlette import status

from api.dependencies import get_assessment_id, get_session
from api.models.answer import Answer
from api.models.mark import Mark, MarkHistory
from api.schemas.answer import AnswerRead
from api.schemas.mark import (
    MarkRead,
    MarkWrite,
    MarkWrite_,
)

marking_all_router = APIRouter(tags=["marking"])


@marking_all_router.get(
    "/marks",
    response_model=list[MarkRead],
    summary="Retrieve marks and feedback for exam questions",
    description="Retrieve latest marks and feedback (with corresponding history)",
)
def get_marks(
    student_username: str | None = None,
    session: Session = Depends(get_session),
    assessment_id: str = Depends(get_assessment_id),
):
    query = (
        select(Mark)
        .where(Mark.exam_id == assessment_id)
        .order_by(Mark.question, Mark.part, Mark.section)  # type: ignore
    )
    if student_username:
        query = query.where(Mark.username == student_username)
    return session.exec(query).all()


@marking_all_router.post(
    "/marks",
    response_model=MarkRead,
    summary="Record section mark and/or feedback for student",
    description="""
Record a mark and/or feedback comment on a specific section of the given student's exam submission.
""",
)
def post_mark_for_section(
    payload: MarkWrite_,
    session: Session = Depends(get_session),
    assessment_id: str = Depends(get_assessment_id),
):
    if payload.mark is None and not payload.feedback:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="At least one between 'mark' and 'feedback' is required.",
        )

    query = select(Mark).where(
        Mark.exam_id == assessment_id,
        Mark.username == payload.username,
        Mark.question == payload.question,
        Mark.part == payload.part,
        Mark.section == payload.section,
    )
    mark = session.exec(query).first()
    if mark:
        mark.mark = payload.mark if payload.mark is not None else mark.mark
        mark.feedback = (
            payload.feedback if payload.feedback is not None else mark.feedback
        )
        mark.timestamp = datetime.now(timezone.utc).replace(tzinfo=None)
        mark.marker = "adumble"  # Currently hardcoded
    else:
        mark = Mark(
            exam_id=assessment_id,
            question=payload.question,
            part=payload.part,
            section=payload.section,
            mark=payload.mark,
            feedback=payload.feedback,
            username=payload.username,
            marker="adumble",
        )
        session.add(mark)
    session.add(
        MarkHistory(
            current_mark=mark,
            mark=payload.mark,
            feedback=payload.feedback,
            marker=mark.marker,
            timestamp=mark.timestamp,
        )
    )
    session.commit()
    return mark


@marking_all_router.get(
    "/answers",
    response_model=list[AnswerRead],
    summary="Retrieve student answers for all questions in exam",
    description="Retrieve the latest answers for all questions in exam",
)
def get_answers(
    student_username: str | None = None,
    session: Session = Depends(get_session),
    assessment_id: str = Depends(get_assessment_id),
):
    query = (
        select(Answer)
        .where(Answer.exam_id == assessment_id)
        .order_by(Answer.question, Answer.part, Answer.section, Answer.task)  # type: ignore
    )
    if student_username:
        query = query.where(Answer.username == student_username)
    return session.exec(query).all()
