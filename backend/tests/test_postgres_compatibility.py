import os
import pytest
from sqlalchemy import create_engine, text
from app.core.config import Settings, normalize_postgres_url
from app.db.base import Base
import app.models
from app.db.migrate_sqlite_to_postgres import (
    sanitize_value_for_postgres,
    parse_date_or_datetime,
    migrate_data,
)


def test_postgres_url_normalization():
    """Verify that postgresql:// and postgres:// URLs are normalized to postgresql+psycopg://."""
    url1 = "postgresql://postgres.user:pass@aws-0-ap-south-1.pooler.supabase.com:6543/postgres"
    norm1 = normalize_postgres_url(url1)
    assert norm1.startswith("postgresql+psycopg://")
    assert "pooler.supabase.com" in norm1

    url2 = "postgres://postgres.user:pass@aws-0-ap-south-1.pooler.supabase.com:5432/postgres"
    norm2 = normalize_postgres_url(url2)
    assert norm2.startswith("postgresql+psycopg://")

    # Already formatted URL should remain untouched
    url3 = "postgresql+psycopg://postgres.user:pass@aws-0-ap-south-1.pooler.supabase.com:6543/postgres?pgbouncer=true"
    assert normalize_postgres_url(url3) == url3

    # SQLite URLs should remain untouched
    sqlite_url = "sqlite:///./health_saathi.db"
    assert normalize_postgres_url(sqlite_url) == sqlite_url


def test_psycopg3_dialect_and_engine_config():
    """Verify psycopg3 driver is loaded and engine arguments are properly configured for Supabase."""
    sample_pg_url = "postgresql+psycopg://postgres.user:pass@aws-0-ap-south-1.pooler.supabase.com:6543/postgres?pgbouncer=true"
    engine = create_engine(
        sample_pg_url,
        connect_args={"prepare_threshold": None},
        pool_pre_ping=True
    )
    assert engine.dialect.name == "postgresql"
    assert engine.dialect.driver == "psycopg"
    assert engine.pool is not None


def test_sanitize_values_for_postgres():
    """Verify boolean and date conversions for PostgreSQL."""
    assert sanitize_value_for_postgres("is_active", 1) is True
    assert sanitize_value_for_postgres("is_active", 0) is False
    assert sanitize_value_for_postgres("is_verified", "true") is True
    assert sanitize_value_for_postgres("is_verified", "0") is False
    assert sanitize_value_for_postgres("consent_given", 1) is True

    # Dates and timestamps
    dt = parse_date_or_datetime("2026-10-10 12:30:00")
    assert dt is not None
    assert dt.year == 2026 and dt.month == 10 and dt.day == 10

    d = parse_date_or_datetime("2026-09-25")
    assert d is not None
    assert d.year == 2026 and d.month == 9 and d.day == 25


def test_data_migration_idempotent(tmp_path):
    """Verify data migration transfers rows, preserves integrity, and skips existing rows on rerun."""
    test_db_path = str(tmp_path / "test_target.db")
    target_url = f"sqlite:///{test_db_path}"

    target_engine = create_engine(target_url)
    Base.metadata.create_all(bind=target_engine)

    # First run: should insert rows
    source_sqlite = os.path.abspath("health_saathi.db")
    if not os.path.exists(source_sqlite):
        pytest.skip("health_saathi.db not found for data migration test")

    res1 = migrate_data(
        sqlite_path=source_sqlite,
        target_url=target_url,
        dry_run=False
    )
    assert len(res1) > 0
    assert res1["users"]["inserted"] >= 1

    # Second run: should be completely idempotent (all existing rows skipped, 0 new inserts)
    res2 = migrate_data(
        sqlite_path=source_sqlite,
        target_url=target_url,
        dry_run=False
    )
    assert res2["users"]["inserted"] == 0
    assert res2["users"]["skipped"] >= 1
