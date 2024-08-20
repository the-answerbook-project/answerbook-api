from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from starlette import status

from api.dependencies import (
    get_assessment_config,
    get_assessment_spec,
    get_session,
    verify_user_is_marker,
)
from api.models.answer import Answer
from api.models.assessment import Assessment
from api.models.mark import Mark, MarkHistory
from api.models.student import Student
from api.schemas.answer import AnswerRead
from api.schemas.exam import AssessmentSpec, Question
from api.schemas.mark import (
    MarkRead,
    MarkWrite,
)

marking_router = APIRouter(
    prefix="/{assessment_code}",
    tags=["marking"],
)


@marking_router.get(
    "/marks",
    response_model=list[MarkRead],
    summary="Retrieve marks and feedback for the assessment",
    description="Retrieve latest marks and feedback (with corresponding history)",
)
def get_marks(
    assessment_code: str,
    student_username: str | None = None,
    _=Depends(verify_user_is_marker),
    session: Session = Depends(get_session),
):
    query = (
        select(Mark)
        .where(Mark.exam_id == assessment_code)
        .order_by(Mark.question, Mark.part, Mark.section)  # type: ignore
    )
    if student_username:
        query = query.where(Mark.username == student_username)
    return session.exec(query).all()


@marking_router.post(
    "/marks",
    response_model=MarkRead,
    summary="Record section mark and/or feedback for student",
    description="Record a mark and/or feedback comment on a specific section of the given student's submission.",
)
def post_mark_for_section(
    payload: MarkWrite,
    assessment: Assessment = Depends(get_assessment_config),
    session: Session = Depends(get_session),
    marker=Depends(verify_user_is_marker),
):
    if payload.mark is None and not payload.feedback:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="At least one between 'mark' and 'feedback' is required.",
        )

    query = select(Mark).where(
        Mark.assessment_id == assessment.id,
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
        mark.marker = marker
    else:
        mark = Mark(
            exam_id=assessment.code,
            assessment_id=assessment.id,
            question=payload.question,
            part=payload.part,
            section=payload.section,
            mark=payload.mark,
            feedback=payload.feedback,
            username=payload.username,
            marker=marker,
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
    description="Retrieve the latest answers for all questions in exam",
)
def get_answers(
    assessment_code: str,
    student_username: str | None = None,
    session: Session = Depends(get_session),
    _=Depends(verify_user_is_marker),
):
    query = (
        select(Answer)
        .where(Answer.exam_id == assessment_code)
        .order_by(Answer.question, Answer.part, Answer.section, Answer.task)  # type: ignore
    )
    if student_username:
        query = query.where(Answer.username == student_username)
    return session.exec(query).all()


@marking_router.get(
    "/students",
    response_model=list[Student],
    summary="Assessment students",
    description="Retrieve all the students enrolled for the assessment",
)
def get_students(
    config: Assessment = Depends(get_assessment_config),
    _=Depends(verify_user_is_marker),
):
    return config.candidates


@marking_router.get(
    "/questions",
    response_model=dict[int, Question],
    summary="Assessment questions",
    description="Retrieve all the assessment questions.",
)
def get_questions(
    assessment: AssessmentSpec = Depends(get_assessment_spec),
    _=Depends(verify_user_is_marker),
):
    return assessment.questions
