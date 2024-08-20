"""add default value to timestamp column in answer table

Revision ID: 636d35aa928b
Revises: 78efc3ae4af7
Create Date: 2024-08-20 17:36:55.671887

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "636d35aa928b"
down_revision: Union[str, None] = "78efc3ae4af7"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column(
        "answer",
        "timestamp",
        existing_type=postgresql.TIMESTAMP(),
        server_default=sa.text("timezone('UTC', CURRENT_TIMESTAMP)"),
        nullable=False,
    )


def downgrade() -> None:
    pass
