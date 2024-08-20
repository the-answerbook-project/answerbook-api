from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from starlette import status

from api.dependencies import get_assessment_id, get_session
from api.models.answer import Answer
from api.models.assessment import Assessment
from api.schemas.answer import AnswerRead, AnswerWrite

answers_router = APIRouter(prefix="/answers/{username}", tags=["exam"])


@answers_router.get(
    "/question/{question_number}/part/{part_number}/section/{section_number}",
    summary="Retrieve user answer to a section of a part of a question",
    description="""
		Retrieve the latest user answer to the given question-part-section.
		""",
)
def get_qpsa(
    username: str,
    question_number: int,
    part_number: int,
    section_number: int,
    session: Session = Depends(get_session),
    assessment_id: str = Depends(get_assessment_id),
):
    query = (
        select(Answer)
        .where(
            Answer.exam_id == assessment_id,
            Answer.question == question_number,
            Answer.part == part_number,
            Answer.section == section_number,
            Answer.username == username,
        )
        .order_by(Answer.task)  # type: ignore
    )
    return session.exec(query).all()


@answers_router.get(
    "/question/{question_number}",
    response_model=list[AnswerRead],
    summary="Retrieve user answer to question",
    description="""
Retrieve the latest user answer to the given question's tasks.
""",
)
def get_answer_to_question(
    question_number: int,
    username: str,
    session: Session = Depends(get_session),
    assessment_id: str = Depends(get_assessment_id),
):
    query = (
        select(Answer)
        .where(
            Answer.question == question_number,
            Answer.exam_id == assessment_id,
            Answer.username == username,
        )
        .order_by(Answer.part, Answer.section, Answer.task)  # type: ignore
    )
    return session.exec(query).all()


@answers_router.post(
    "/question/{question_number}",
    # response_model=AnswerRead,
    summary="Submit user answer to question",
    description="""
Submit the user answer to the given question's task.
""",
)
def submit_answer_to_question(
    question_number: int,
    username: str,
    answers: list[AnswerWrite],
    session: Session = Depends(get_session),
    assessment_id: str = Depends(get_assessment_id),
):
    assessment_query = select(Assessment).where(Assessment.code == assessment_id)
    assessment = session.exec(assessment_query).first()
    if assessment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assessment not found.",
        )

    answer_objects: list[Answer] = [
        Answer(
            **answer.model_dump(),
            assessment_id=assessment.id,
            exam_id=assessment_id,
            username=username,
        )
        for answer in answers
    ]

    for answer in answer_objects:
        # Check if there based on the exam_id, username, question, part, section, task
        # Update if so
        # Otherwise, insert
        query = select(Answer).where(
            Answer.assessment_id == assessment.id,
            Answer.username == username,
            Answer.question == question_number,
            Answer.part == answer.part,
            Answer.section == answer.section,
            Answer.task == answer.task,
        )
        existing_answer = session.exec(query).first()
        if existing_answer:
            existing_answer.answer = answer.answer
        else:
            session.add(answer)

    return {}
