"""add assessment_id column to answer table

Revision ID: b4ac26635c45
Revises: f461f0fec2a9
Create Date: 2024-08-20 12:36:49.730602

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy import text

# revision identifiers, used by Alembic.
revision: str = "b4ac26635c45"
down_revision: Union[str, None] = "f461f0fec2a9"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("answer", sa.Column("assessment_id", sa.Integer(), nullable=True))
    op.create_index(
        op.f("ix_answer_assessment_id"), "answer", ["assessment_id"], unique=False
    )
    op.create_foreign_key(None, "answer", "assessment", ["assessment_id"], ["id"])

    bind = op.get_bind()
    bind.execute(
        text(
            "UPDATE answer SET assessment_id = (SELECT assessment.id FROM assessment WHERE assessment.code = answer.exam_id)"
        )
    )

    op.alter_column("answer", "assessment_id", nullable=False)


def downgrade() -> None:
    op.drop_constraint("answer_assessment_id_fkey", "answer", type_="foreignkey")
    op.drop_index(op.f("ix_answer_assessment_id"), table_name="answer")
    op.drop_column("answer", "assessment_id")
