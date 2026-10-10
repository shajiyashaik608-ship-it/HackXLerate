from typing import Generator, Dict, Any
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from app.core.config import settings
from app.core.logging import logger

connect_args: Dict[str, Any] = {}
engine_kwargs: Dict[str, Any] = {
    "pool_pre_ping": True,
}

if settings.DATABASE_URL.startswith("sqlite"):
    connect_args["check_same_thread"] = False
else:
    # Supabase PostgreSQL configuration
    # For psycopg v3 through PgBouncer transaction pooler (port 6543),
    # disable prepared statement caching to prevent 'prepared statement already exists' collisions.
    if "psycopg" in settings.DATABASE_URL or "postgresql" in settings.DATABASE_URL:
        connect_args["prepare_threshold"] = None
    
    engine_kwargs.update({
        "pool_size": getattr(settings, "DATABASE_POOL_SIZE", 10),
        "max_overflow": getattr(settings, "DATABASE_MAX_OVERFLOW", 20),
        "pool_timeout": getattr(settings, "DATABASE_POOL_TIMEOUT", 30),
        "pool_recycle": getattr(settings, "DATABASE_POOL_RECYCLE", 1800),
    })

engine = create_engine(
    settings.DATABASE_URL,
    connect_args=connect_args,
    **engine_kwargs
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    class_=Session
)


def get_db() -> Generator[Session, None, None]:
    """Dependency that provides an active database session per request."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

