"""add unique constraint to student username

Revision ID: a43ab9fdd90e
Revises: 905a24c008fc
Create Date: 2024-07-10 11:44:03.569639

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "a43ab9fdd90e"
down_revision: Union[str, None] = "905a24c008fc"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_unique_constraint(None, "student", ["username"])


def downgrade() -> None:
    op.drop_constraint("student_username_key", "student", type_="unique")
