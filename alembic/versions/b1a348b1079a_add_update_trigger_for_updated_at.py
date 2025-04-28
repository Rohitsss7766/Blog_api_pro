"""add update trigger for updated_at

Revision ID: b1a348b1079a
Revises: a1e0ad4d2842
Create Date: 2025-04-15 13:40:48.524643

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa



# revision identifiers, used by Alembic.
revision: str = 'b1a348b1079a'
down_revision: Union[str, None] = 'a1e0ad4d2842'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # SQL function
    op.execute("""
    CREATE OR REPLACE FUNCTION update_updated_at_column()
    RETURNS TRIGGER AS $$
    BEGIN
        NEW.updated_at = now();
        RETURN NEW;
    END;
    $$ language 'plpgsql';
    """)

    # Trigger
    op.execute("""
    CREATE TRIGGER update_posts_updated_at
    BEFORE UPDATE ON posts
    FOR EACH ROW
    EXECUTE PROCEDURE update_updated_at_column();
    """)

def downgrade():
    op.execute("DROP TRIGGER IF EXISTS update_post_updated_at ON posts;")
    op.execute("DROP FUNCTION IF EXISTS update_updated_at_column;")
