"""add marker table

Revision ID: f461f0fec2a9
Revises: cc42389e37d6
Create Date: 2024-08-14 17:05:01.198703

"""

from typing import Sequence, Union

import sqlalchemy as sa
import sqlmodel
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "f461f0fec2a9"
down_revision: Union[str, None] = "cc42389e37d6"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "marker",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("assessment_id", sa.Integer(), nullable=False),
        sa.Column("username", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("firstname", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("lastname", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.ForeignKeyConstraint(
            ["assessment_id"],
            ["assessment.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("username"),
    )
    op.create_index(
        op.f("ix_marker_assessment_id"), "marker", ["assessment_id"], unique=False
    )


def downgrade() -> None:
    op.drop_index(op.f("ix_marker_assessment_id"), table_name="marker")
    op.drop_table("marker")
