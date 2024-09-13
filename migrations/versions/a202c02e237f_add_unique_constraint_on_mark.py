"""add unique constraint on mark

Revision ID: a202c02e237f
Revises: b0692e4ee910
Create Date: 2024-08-28 14:07:45.689643

"""

from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "a202c02e237f"
down_revision: Union[str, None] = "b0692e4ee910"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_unique_constraint(
        "mark_assessment_id_username_question_part_section_key",
        "mark",
        ["assessment_id", "username", "question", "part", "section"],
    )


def downgrade() -> None:
    op.drop_constraint(
        "mark_assessment_id_username_question_part_section_key", "mark", type_="unique"
    )
