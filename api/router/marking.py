from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from starlette import status

from api.dependencies import get_assessment_id, get_session
from api.schemas.answer import Answer, AnswerRead
from api.schemas.mark import (
    Mark,
    MarkHistory,
    MarkRead,
    MarkWrite,
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


@marking_router.post(
    "/marks",
    response_model=MarkRead,
    summary="Record section mark and/or feedback for student",
    description="""
Record a mark and/or feedback comment on a specific section of the given student's exam submission.
""",
)
def post_mark_for_section(
    student_username: str,
    payload: MarkWrite,
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
        Mark.username == student_username,
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
            username=student_username,
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
