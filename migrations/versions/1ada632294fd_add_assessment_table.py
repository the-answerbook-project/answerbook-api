"""add assessment table

Revision ID: 1ada632294fd
Revises: a6d3be52d408
Create Date: 2024-07-11 12:31:09.815680

"""

from typing import Sequence, Union

import sqlalchemy as sa
import sqlmodel
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "1ada632294fd"
down_revision: Union[str, None] = "a6d3be52d408"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "assessment",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("exam_code", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column(
            "authentication_mode",
            sa.Enum("LDAP", "INTERNAL", name="authentication_mode"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_assessment_exam_code"), "assessment", ["exam_code"], unique=False
    )


def downgrade() -> None:
    op.drop_index(op.f("ix_assessment_exam_code"), table_name="assessment")
    op.drop_table("assessment")
    op.execute("DROP TYPE authentication_mode")
