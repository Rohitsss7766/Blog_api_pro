from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context
import sys
import os

# Add your app path so Alembic can find your models
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import your database Base and engine
from dotenv import load_dotenv
load_dotenv()

from app.database import Base
from app import models  # Ensure models are imported so Alembic detects them

# Alembic Config object
config = context.config

# Setup logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Set the metadata for Alembic autogeneration
target_metadata = Base.metadata

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = os.getenv("DATABASE_URL")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode."""
    # Load the database URL from the environment variable
    url = os.getenv("DATABASE_URL")
    
    # Ensure that the URL is properly formatted
    if not url:
        raise ValueError("DATABASE_URL not set in the environment")

    # Create the engine using the provided URL
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix='sqlalchemy.',
        poolclass=pool.NullPool,
        url=url  # Pass the URL directly here
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True  # Optional: detects column type changes
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
