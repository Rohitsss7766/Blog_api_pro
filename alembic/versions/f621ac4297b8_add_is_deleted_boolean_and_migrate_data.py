"""Add is_deleted boolean and migrate data

Revision ID: f621ac4297b8
Revises: 55dc1954db5c
Create Date: 2025-04-15 15:01:38.166103

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f621ac4297b8'
down_revision: Union[str, None] = '55dc1954db5c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
