"""Add default rows and stored procedure

Revision ID: 72fe27c02489
Revises: f621ac4297b8
Create Date: 2025-04-15 16:56:49.757598

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa



# revision identifiers, used by Alembic.
revision: str = '72fe27c02489'
down_revision: Union[str, None] = 'f621ac4297b8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():


    op.create_table(
        'deleted_posts_log',
        sa.Column('id', sa.Integer),
        sa.Column('title', sa.Text),
        sa.Column('author', sa.Text),
        sa.Column('deleted_on', sa.DateTime, server_default=sa.text('NOW()')),
        schema='public'
    )



    op.execute("""
        
        END;CREATE OR REPLACE PROCEDURE public.get_deleted_posts_proc()
        LANGUAGE plpgsql
        AS $$
        BEGIN
            INSERT INTO public.deleted_posts_log (id, title, author)
            SELECT id, title::TEXT, author::TEXT
            FROM public.posts
            WHERE is_deleted = TRUE;
        $$;
    """)

    # Inserting two default rows into the 'post' table
    op.execute("""
        INSERT INTO posts (title, content, author, created_at, updated_at, is_deleted, summary)
        VALUES 
        ('Welcome Post', 'This is the first default post.', 'Admin',  now()::timestamp, now()::timestamp, false::boolean,'Intro post'),
        ('Second Post', 'Another starter post.', 'Admin', now()::timestamp, now()::timestamp, false::boolean, 'Sample post');
    """)

    # Creating stored procedure to get deleted posts
    op.execute("""
DROP FUNCTION IF EXISTS public.get_deleted_posts();

CREATE OR REPLACE FUNCTION public.get_deleted_posts()
RETURNS TABLE (
    id INT, 
    title VARCHAR(200), 
    author VARCHAR(100)
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY 
    SELECT p.id, p.title, p.author 
    FROM public.posts p 
    WHERE p.is_deleted = TRUE;
END;
$$;

ALTER FUNCTION public.get_deleted_posts()
OWNER TO postgres;
""")


def downgrade():
    # Optionally, rollback the changes (e.g., removing rows or stored procedure)
    op.execute("DROP FUNCTION IF EXISTS get_deleted_posts")
    op.execute("DELETE FROM posts WHERE title = 'Welcome Post' OR title = 'Second Post'")
    op.execute("DROP PROCEDURE IF EXISTS public.get_deleted_posts_proc();")
    op.drop_table('deleted_posts_log', schema='public')
