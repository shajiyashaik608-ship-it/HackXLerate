from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
import os
import sys

# Ensure backend root is on sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from app.core.config import settings
from app.db.base import Base
import app.models  # Load all models into Base.metadata

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata

# Determine target database connection URL for migrations:
# Prioritize DIRECT_URL (session pooler port 5432) for DDL operations if configured,
# falling back to DATABASE_URL.
migration_url = (
    os.environ.get("DIRECT_URL")
    or getattr(settings, "DIRECT_URL", None)
    or os.environ.get("DATABASE_URL")
    or getattr(settings, "DATABASE_URL", None)
)

if migration_url:
    # Ensure psycopg 3 driver prefix is applied if standard postgresql:// was provided
    if migration_url.startswith("postgresql://"):
        migration_url = "postgresql+psycopg://" + migration_url[len("postgresql://"):]
    elif migration_url.startswith("postgres://"):
        migration_url = "postgresql+psycopg://" + migration_url[len("postgres://"):]
    config.set_main_option("sqlalchemy.url", migration_url)


def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
