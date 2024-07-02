from fastapi import APIRouter

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
):
    return []
