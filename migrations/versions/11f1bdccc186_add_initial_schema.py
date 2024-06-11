"""Add initial schema

Revision ID: 11f1bdccc186
Revises:
Create Date: 2024-06-10 21:36:25.733354

"""

from typing import Sequence, Union

import sqlalchemy as sa
import sqlmodel
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "11f1bdccc186"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "answer",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("exam_id", sa.Integer(), nullable=False),
        sa.Column("username", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("question", sa.Integer(), nullable=False),
        sa.Column("part", sa.Integer(), nullable=False),
        sa.Column("section", sa.Integer(), nullable=False),
        sa.Column("task", sa.Integer(), nullable=False),
        sa.Column("answer", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("timestamp", sa.DateTime(), nullable=True),
        sa.Column("ip", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("answer")
    # ### end Alembic commands ###