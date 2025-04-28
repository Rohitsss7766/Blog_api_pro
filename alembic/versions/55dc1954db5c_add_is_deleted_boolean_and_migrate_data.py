"""Add is_deleted boolean and migrate data

Revision ID: 55dc1954db5c
Revises: 35850e8d3d07
Create Date: 2025-04-15 14:59:16.510207
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '55dc1954db5c'
down_revision: Union[str, None] = '35850e8d3d07'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Step 1: Add is_deleted column with default False
    op.add_column('posts', sa.Column('is_deleted', sa.Boolean(), nullable=False, server_default=sa.text('false')))

    # Step 2: Update is_deleted = True where deleted_at IS NOT NULL
    op.execute("UPDATE posts SET is_deleted = TRUE WHERE deleted_at IS NOT NULL")

    # Step 3: Drop deleted_at column
    op.drop_column('posts', 'deleted_at')


def downgrade():
    # Step 1: Re-add deleted_at column
    op.add_column('posts', sa.Column('deleted_at', sa.DateTime(), nullable=True))

    # Step 2: Restore deleted_at values as now() for those soft deleted
    op.execute("UPDATE posts SET deleted_at = NOW() WHERE is_deleted = TRUE")

    # Step 3: Drop is_deleted column
    op.drop_column('posts', 'is_deleted')
