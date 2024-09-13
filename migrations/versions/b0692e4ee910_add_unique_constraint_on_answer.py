"""add unique constraint on answer

Revision ID: b0692e4ee910
Revises: 3bf6fdce1c45
Create Date: 2024-08-28 13:55:11.612368

"""

from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "b0692e4ee910"
down_revision: Union[str, None] = "3bf6fdce1c45"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_unique_constraint(
        "answer_assessment_id_username_question_part_section_task_key",
        "answer",
        ["assessment_id", "username", "question", "part", "section", "task"],
    )


def downgrade() -> None:
    op.drop_constraint(
        "answer_assessment_id_username_question_part_section_task_key",
        "answer",
        type_="unique",
    )
