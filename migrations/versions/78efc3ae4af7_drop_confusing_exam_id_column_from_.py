"""drop confusing exam_id column from tables

Revision ID: 78efc3ae4af7
Revises: 71f5d28220b5
Create Date: 2024-08-20 15:17:27.529230

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy import text

# revision identifiers, used by Alembic.
revision: str = "78efc3ae4af7"
down_revision: Union[str, None] = "71f5d28220b5"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_index("ix_answer_exam_id", table_name="answer")
    op.drop_column("answer", "exam_id")
    op.drop_index("ix_mark_exam_id", table_name="mark")
    op.drop_column("mark", "exam_id")
    op.drop_index("ix_student_exam_id", table_name="student")
    op.drop_column("student", "exam_id")


def downgrade() -> None:
    # student ------------
    op.add_column(
        "student",
        sa.Column("exam_id", sa.VARCHAR(), autoincrement=False, nullable=True),
    )
    bind = op.get_bind()
    bind.execute(
        text(
            "UPDATE student SET exam_id = (SELECT assessment.code FROM assessment WHERE assessment.id = student.assessment_id)"
        )
    )
    op.create_index("ix_student_exam_id", "student", ["exam_id"], unique=False)
    op.alter_column("student", "exam_id", nullable=False)
    # mark ------------
    op.add_column(
        "mark", sa.Column("exam_id", sa.VARCHAR(), autoincrement=False, nullable=True)
    )
    bind = op.get_bind()
    bind.execute(
        text(
            "UPDATE mark SET exam_id = (SELECT assessment.code FROM assessment WHERE assessment.id = mark.assessment_id)"
        )
    )
    op.create_index("ix_mark_exam_id", "mark", ["exam_id"], unique=False)
    op.alter_column("mark", "exam_id", nullable=False)
    # answer ------------
    op.add_column(
        "answer", sa.Column("exam_id", sa.VARCHAR(), autoincrement=False, nullable=True)
    )
    bind = op.get_bind()
    bind.execute(
        text(
            "UPDATE answer SET exam_id = (SELECT assessment.code FROM assessment WHERE assessment.id = answer.assessment_id)"
        )
    )
    op.create_index("ix_answer_exam_id", "answer", ["exam_id"], unique=False)
    op.alter_column("answer", "exam_id", nullable=False)
