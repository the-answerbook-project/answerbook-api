from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from api.authentication.jwt_utils import JwtSubject
from api.dependencies import (
    get_assessment_spec,
    get_session,
    validate_token,
)
from api.models.answer import Answer
from api.schemas.answer import AnswerRead
from api.schemas.exam import AssessmentHeading, AssessmentSpec
from api.utils import parse_interval

candidates_router = APIRouter(
    prefix="/{assessment_code}/candidates/me", tags=["candidates"]
)


@candidates_router.get(
    "/heading",
    response_model=AssessmentHeading,
    summary="Assessment heading",
    description="Retrieve the assessment heading with user-specific start-time and end-time.",
)
def get_user_specific_assessment_heading(
    assessment: AssessmentSpec = Depends(get_assessment_spec),
    sub: JwtSubject = Depends(validate_token),
):
    assessment.begins = assessment.computed_beginning_for_candidate(sub.username)
    assessment.duration = assessment.computed_duration_for_candidate(sub.username)
    return AssessmentHeading(**assessment.model_dump())


@candidates_router.get(
    "/answers",
    response_model=list[AnswerRead],
    summary="User's answers to assessments' tasks",
    description="Retrieve all the user's answers to the assessment.",
)
def get_user_answers(
    assessment_code: str,
    session: Session = Depends(get_session),
    sub: JwtSubject = Depends(validate_token),
):
    query = (
        select(Answer)
        .where(Answer.exam_id == assessment_code, Answer.username == sub.username)
        .order_by(Answer.question, Answer.part, Answer.section, Answer.task)  # type: ignore
    )
    return session.exec(query).all()
