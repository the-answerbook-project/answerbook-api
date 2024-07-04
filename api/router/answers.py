from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from api.dependencies import get_assessment_id, get_session
from api.models.answer import Answer
from api.schemas.answer import AnswerRead

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
    answers: list[AnswerRead],
    session: Session = Depends(get_session),
    assessment_id: str = Depends(get_assessment_id),
):
    answer_objects: list[Answer] = [
        Answer(**answer.dict(), exam_id=assessment_id, username="hpotter")
        for answer in answers
    ]

    for answer in answer_objects:
        # Check if there based on the exam_id, username, question, part, section, task
        # Update if so
        # Otherwise, insert
        query = select(Answer).where(
            Answer.exam_id == assessment_id,
            Answer.username == "hpotter",
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
