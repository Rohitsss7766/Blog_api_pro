"""add deleted_at column

Revision ID: 0d5d4a0ecc92
Revises: b1a348b1079a
Create Date: 2025-04-15 14:12:53.212255

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '0d5d4a0ecc92'
down_revision: Union[str, None] = 'b1a348b1079a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('posts', 'deleted_at',
               existing_type=postgresql.BOOLEAN(),
               existing_type_=sa.Boolean(),
               server_default = None,
               existing_nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('posts', 'deleted_at',
               existing_type=postgresql.BOOLEAN(),
               existing_type_=sa.Boolean(),
               server_default = None,
               existing_nullable=True)
    # ### end Alembic commands ###
