from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from api.dependencies import get_assessment_id, get_session
from api.schemas.answer import Answer, AnswerRead

answer_router = APIRouter(prefix="/answers", tags=["answers"])


@answer_router.get(
    "/{student_username}",
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
