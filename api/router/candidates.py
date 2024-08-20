from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from starlette import status

from api.authentication.jwt_utils import JwtSubject
from api.dependencies import (
    get_assessment_config,
    get_assessment_spec,
    get_session,
    validate_token,
)
from api.models.answer import Answer
from api.models.assessment import Assessment
from api.schemas.answer import AnswerRead, AnswerWrite
from api.schemas.exam import AssessmentHeading, AssessmentSpec, Question

candidates_router = APIRouter(
    prefix="/{assessment_code}/candidates/me", tags=["candidates"]
)

GRACE_PERIOD_IN_SECONDS_PAST_DEADLINE = 30


@candidates_router.get(
    "/heading",
    response_model=AssessmentHeading,
    summary="Assessment heading",
    description="Retrieve the assessment heading with user-specific start-time and end-time.",
)
def get_assessment_heading(
    assessment: AssessmentSpec = Depends(get_assessment_spec),
    sub: JwtSubject = Depends(validate_token),
):
    assessment.begins = assessment.computed_beginning_for_candidate(sub.username)
    assessment.duration = assessment.computed_duration_for_candidate(sub.username)
    return AssessmentHeading(**assessment.model_dump())


@candidates_router.get(
    "/questions",
    response_model=dict[int, Question],
    summary="Assessment questions",
    description="Retrieve all the assessment questions.",
)
def get_questions(
    assessment: AssessmentSpec = Depends(get_assessment_spec),
    subject: JwtSubject = Depends(validate_token),
):
    start_time = assessment.computed_beginning_for_candidate(subject.username)
    if datetime.now(tz=timezone.utc) < start_time:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The assessment has not started yet.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return assessment.questions


@candidates_router.get(
    "/answers",
    response_model=list[AnswerRead],
    summary="User's answers to assessments' tasks",
    description="Retrieve all the user's answers to the assessment.",
)
def get_answers(
    assessment: Assessment = Depends(get_assessment_config),
    session: Session = Depends(get_session),
    sub: JwtSubject = Depends(validate_token),
):
    query = (
        select(Answer)
        .where(Answer.assessment_id == assessment.id, Answer.username == sub.username)
        .order_by(Answer.question, Answer.part, Answer.section, Answer.task)  # type: ignore
    )
    return session.exec(query).all()


@candidates_router.post(
    "/answers",
    response_model=AnswerRead,
    summary="Store candidate's answer",
    description="Store the candidate's answer to a specific assessment's task.",
)
def post_answer(
    answer: AnswerWrite,
    assessment_spec: AssessmentSpec = Depends(get_assessment_spec),
    assessment_config: Assessment = Depends(get_assessment_config),
    session: Session = Depends(get_session),
    subject: JwtSubject = Depends(validate_token),
):
    start_time = assessment_spec.computed_beginning_for_candidate(subject.username)
    if datetime.now(tz=timezone.utc) < start_time:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The assessment has not started yet.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    end_time = assessment_spec.computed_end_time_for_candidate(subject.username)
    end_time += timedelta(seconds=GRACE_PERIOD_IN_SECONDS_PAST_DEADLINE)
    if datetime.now(tz=timezone.utc) > end_time:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The assessment is over.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    new_answer = Answer(
        assessment_id=assessment_config.id,
        username=subject.username,
        **answer.model_dump(),
    )
    session.add(new_answer)
    session.commit()
    return new_answer
