from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from api.dependencies import get_assessment_id, get_session
from api.models.answer import Answer

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
