"""change deleted_at to is_deleted boolean

Revision ID: 35850e8d3d07
Revises: aae797ed2b5c
Create Date: 2025-04-15 14:51:26.324204

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '35850e8d3d07'
down_revision: Union[str, None] = 'aae797ed2b5c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Step 1: Add new is_deleted column with default False
    with op.batch_alter_table('posts') as batch_op:
        batch_op.add_column(sa.Column('is_deleted', sa.Boolean(), nullable=False, server_default=sa.text('false')))

    # Step 2: Update is_deleted to True for rows where deleted_at is NOT NULL
    op.execute("UPDATE posts SET is_deleted = TRUE WHERE deleted_at IS NOT NULL")

    # Step 3: Drop deleted_at column
    with op.batch_alter_table('posts') as batch_op:
        batch_op.drop_column('deleted_at')


def downgrade():
    # Step 1: Re-add deleted_at column
    with op.batch_alter_table('posts') as batch_op:
        batch_op.add_column(sa.Column('deleted_at', sa.DateTime(), nullable=True))

    # Step 2: Restore deleted_at values for soft-deleted rows
    op.execute("UPDATE posts SET deleted_at = NOW() WHERE is_deleted = TRUE")

    # Step 3: Drop is_deleted column
    with op.batch_alter_table('posts') as batch_op:
        batch_op.drop_column('is_deleted')

def downgrade() -> None:
    with op.batch_alter_table('posts') as batch_op:
        # Recreate the deleted_at column
        batch_op.add_column(sa.Column('deleted_at', sa.DateTime(), nullable=True))

    # Restore deleted_at timestamps (optional – setting all to current timestamp)
    op.execute("UPDATE posts SET deleted_at = NOW() WHERE is_deleted = TRUE")

    # Remove the boolean column
    with op.batch_alter_table('posts') as batch_op:
        batch_op.drop_column('is_deleted')


