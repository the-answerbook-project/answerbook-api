"""remove server default value from mark_history

Revision ID: 3bf6fdce1c45
Revises: da898eb3951b
Create Date: 2024-08-21 13:10:00.472108

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "3bf6fdce1c45"
down_revision: Union[str, None] = "da898eb3951b"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column("mark_history", "timestamp", server_default=None)


def downgrade() -> None:
    op.alter_column(
        "mark_history",
        "timestamp",
        server_default=sa.text("timezone('UTC', CURRENT_TIMESTAMP)"),
    )
