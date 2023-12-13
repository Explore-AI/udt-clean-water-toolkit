"""empty message

Revision ID: 3661e9f1e35b
Revises:
Create Date: 2023-12-13 08:50:30.166906

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "3661e9f1e35b"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "user",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("first_name", sa.String(254), nullable=False),
        sa.Column("last_name", sa.String(254), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column(
            "created_at", sa.DateTime, server_default=sa.func.current_timestamp()
        ),
        sa.Column(
            "modified_at", sa.DateTime, server_default=sa.func.current_timestamp()
        ),
    )


def downgrade() -> None:
    pass
