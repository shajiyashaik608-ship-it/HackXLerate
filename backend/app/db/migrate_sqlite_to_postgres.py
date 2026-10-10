"""
SQLite to Supabase PostgreSQL Migration Utility for Health Saathi (PCOS Saathi)

Features:
- Automated backup of SQLite source database before transfer.
- Inspects schema and migrates 18 entity tables in topological foreign-key order.
- Preserves primary keys, foreign keys, dates, datetimes, booleans, JSON, and Unicode.
- Idempotent: checks for existing primary keys to avoid duplicate insertion on re-runs.
- Transaction management: commits on complete success, rolls back on error.
- Resets/synchronizes PostgreSQL SERIAL sequences (setval) to prevent sequence collisions.
- Privacy & security: completely suppresses passwords, report text, and health data from outputs.
- Post-migration referential integrity and row count parity verification.
"""

import os
import sys
import shutil
import sqlite3
import argparse
from datetime import datetime, date
from typing import Dict, List, Any, Optional, Tuple

# Ensure backend root is on sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from sqlalchemy import create_engine, text, inspect
from app.core.config import settings, normalize_postgres_url
from app.core.logging import logger

# Topological dependency order of tables to respect foreign keys
TABLES_IN_ORDER = [
    "users",
    "health_profiles",
    "medical_documents",
    "biomarkers",
    "cycle_records",
    "symptom_records",
    "meal_items",
    "meal_plans",
    "meal_plan_items",
    "care_reminders",
    "reminder_completions",
    "conversations",
    "chat_messages",
    "consultation_briefs",
    "community_posts",
    "community_replies",
    "content_reports",
    "notifications",
    "alembic_version"
]


def create_sqlite_backup(sqlite_path: str) -> str:
    """Creates a timestamped backup copy of the SQLite database before reading."""
    if not os.path.exists(sqlite_path):
        raise FileNotFoundError(f"Source SQLite database not found at '{sqlite_path}'.")
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = f"{sqlite_path}.{timestamp}.bak"
    shutil.copy2(sqlite_path, backup_path)
    # Also maintain a standard .bak pointer
    static_bak = f"{sqlite_path}.bak"
    shutil.copy2(sqlite_path, static_bak)
    return backup_path


def parse_date_or_datetime(val: Any) -> Any:
    """Parses SQLite string dates/timestamps into Python date/datetime objects for PostgreSQL."""
    if val is None or not isinstance(val, str):
        return val
    val = val.strip()
    if not val:
        return None
    
    # Try parsing full ISO datetime
    for fmt in ("%Y-%m-%d %H:%M:%S.%f", "%Y-%m-%d %H:%M:%S", "%Y-%m-%dT%H:%M:%S.%f", "%Y-%m-%dT%H:%M:%S"):
        try:
            return datetime.strptime(val, fmt)
        except ValueError:
            pass
    # Try parsing date only
    try:
        return datetime.strptime(val, "%Y-%m-%d").date()
    except ValueError:
        pass
    return val


def sanitize_value_for_postgres(col_name: str, val: Any) -> Any:
    """Converts SQLite primitives to PostgreSQL-compliant types (booleans, timestamps, nulls)."""
    if val is None:
        return None
    
    # Boolean conversions
    if col_name.startswith("is_") or col_name in ("consent_given",):
        if isinstance(val, (int, str)):
            return bool(int(val)) if str(val).isdigit() else (str(val).lower() in ("true", "1", "yes"))
        return bool(val)
    
    # Date / Timestamp conversions
    if any(suffix in col_name for suffix in ("_at", "_date", "_time", "occurrence", "until")):
        return parse_date_or_datetime(val)
        
    return val


def migrate_data(
    sqlite_path: str,
    target_url: str,
    dry_run: bool = False,
    verify_only: bool = False
) -> Dict[str, Any]:
    """
    Executes safe SQLite to PostgreSQL data migration.
    """
    normalized_target = normalize_postgres_url(target_url) or target_url
    
    if not os.path.exists(sqlite_path):
        raise FileNotFoundError(f"Source SQLite database '{sqlite_path}' does not exist.")

    # 1. Create SQLite backup
    backup_path = create_sqlite_backup(sqlite_path)
    print(f"[BACKUP] Source SQLite safely backed up to: {backup_path}")

    # 2. Connect to Source SQLite
    sqlite_conn = sqlite3.connect(sqlite_path)
    sqlite_conn.row_factory = sqlite3.Row
    sqlite_cur = sqlite_conn.cursor()

    # 3. Connect to Target Engine
    target_engine = create_engine(
        normalized_target,
        connect_args={"prepare_threshold": None} if "psycopg" in normalized_target else {},
        pool_pre_ping=True
    )

    results: Dict[str, Dict[str, int]] = {}

    with target_engine.connect() as target_conn:
        target_inspector = inspect(target_engine)
        existing_target_tables = target_inspector.get_table_names()

        print("\n" + "=" * 70)
        print(" HEALTH SAATHI: SQLITE -> SUPABASE POSTGRESQL DATA MIGRATION")
        print("=" * 70)
        print(f" Source SQLite  : {sqlite_path}")
        print(f" Target Backend: {target_engine.dialect.name} (mode: {'DRY RUN' if dry_run else 'LIVE TRANSFER'})")
        print("=" * 70 + "\n")

        if verify_only:
            print("[INFO] Running verification checks only...")
            for table in TABLES_IN_ORDER:
                if table not in existing_target_tables:
                    print(f"  [MISSING] Target table '{table}' does not exist in target database.")
                    continue
                sqlite_cur.execute(f"SELECT COUNT(*) FROM \"{table}\"")
                src_count = sqlite_cur.fetchone()[0]
                target_count = target_conn.execute(text(f'SELECT COUNT(*) FROM "{table}"')).scalar()
                print(f"  {table:25} | SQLite: {src_count:4} | Target: {target_count:4}")
            return {"status": "verified"}

        trans = target_conn.begin()
        try:
            for table_name in TABLES_IN_ORDER:
                # Check if table exists in SQLite
                sqlite_cur.execute(
                    "SELECT name FROM sqlite_master WHERE type='table' AND name=?",
                    (table_name,)
                )
                if not sqlite_cur.fetchone():
                    continue

                if table_name not in existing_target_tables:
                    print(f"[SKIP] Target table '{table_name}' does not exist in PostgreSQL. Run Alembic migrations first.")
                    continue

                # Read source rows
                sqlite_cur.execute(f'SELECT * FROM "{table_name}"')
                src_rows = sqlite_cur.fetchall()
                src_count = len(src_rows)

                inserted_count = 0
                skipped_count = 0

                if src_count == 0:
                    results[table_name] = {"source": 0, "inserted": 0, "skipped": 0, "target_total": 0}
                    continue

                col_names = [col[0] for col in sqlite_cur.description]
                pk_col = "version_num" if table_name == "alembic_version" else "id"

                for row in src_rows:
                    row_dict = dict(row)
                    pk_val = row_dict.get(pk_col)

                    # Check idempotency: does record already exist in target?
                    exists = False
                    if pk_val is not None:
                        check_stmt = text(f'SELECT 1 FROM "{table_name}" WHERE "{pk_col}" = :val LIMIT 1')
                        existing_res = target_conn.execute(check_stmt, {"val": pk_val}).scalar()
                        if existing_res:
                            exists = True

                    if exists:
                        skipped_count += 1
                        continue

                    # Sanitize row data
                    clean_dict = {
                        k: sanitize_value_for_postgres(k, v)
                        for k, v in row_dict.items()
                    }

                    if not dry_run:
                        # Build parametrized insert statement
                        cols_sql = ", ".join([f'"{c}"' for c in clean_dict.keys()])
                        vals_sql = ", ".join([f':{c}' for c in clean_dict.keys()])
                        insert_stmt = text(f'INSERT INTO "{table_name}" ({cols_sql}) VALUES ({vals_sql})')
                        target_conn.execute(insert_stmt, clean_dict)

                    inserted_count += 1

                # Sync PostgreSQL serial sequence for tables with integer id
                if not dry_run and pk_col == "id" and target_engine.dialect.name == "postgresql":
                    try:
                        seq_sync_sql = text(f"""
                            SELECT setval(
                                pg_get_serial_sequence('{table_name}', 'id'),
                                COALESCE((SELECT MAX(id) FROM "{table_name}"), 1)
                            );
                        """)
                        target_conn.execute(seq_sync_sql)
                    except Exception as seq_err:
                        # Non-serial primary keys or empty tables
                        pass

                # Verify target total
                target_total = target_conn.execute(text(f'SELECT COUNT(*) FROM "{table_name}"')).scalar() or 0

                results[table_name] = {
                    "source": src_count,
                    "inserted": inserted_count,
                    "skipped": skipped_count,
                    "target_total": target_total
                }

                print(f"  [OK] {table_name:24} | Src: {src_count:3} | Ins: {inserted_count:3} | Skip: {skipped_count:3} | Total: {target_total:3}")

            if dry_run:
                print("\n[DRY RUN] Rolled back all changes. No records written to target.")
                trans.rollback()
            else:
                trans.commit()
                print("\n[SUCCESS] Migration committed successfully to target PostgreSQL database!")

        except Exception as e:
            trans.rollback()
            print(f"\n[ERROR] Migration failed and was rolled back cleanly: {type(e).__name__}: {e}")
            raise e
        finally:
            sqlite_conn.close()

    # 4. Verify Referential Integrity
    verify_referential_integrity(target_engine)
    return results


def verify_referential_integrity(target_engine) -> bool:
    """Verifies that child table records correctly point to existing users."""
    print("\n--- Verifying Referential Integrity ---")
    all_ok = True
    with target_engine.connect() as conn:
        inspector = inspect(target_engine)
        existing_tables = inspector.get_table_names()
        
        user_tables_to_check = [
            "health_profiles",
            "medical_documents",
            "biomarkers",
            "cycle_records",
            "symptom_records",
            "care_reminders",
            "conversations",
            "consultation_briefs",
            "notifications"
        ]
        
        for table in user_tables_to_check:
            if table not in existing_tables or "users" not in existing_tables:
                continue
            orphan_query = text(f"""
                SELECT COUNT(*) FROM "{table}" t
                WHERE t.user_id IS NOT NULL
                  AND NOT EXISTS (SELECT 1 FROM "users" u WHERE u.id = t.user_id)
            """)
            try:
                orphans = conn.execute(orphan_query).scalar() or 0
                if orphans > 0:
                    print(f"  [WARN] {table}: {orphans} orphaned records found!")
                    all_ok = False
                else:
                    print(f"  [OK] {table:24}: 0 orphaned references (Integrity Verified)")
            except Exception:
                pass
    return all_ok


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Health Saathi SQLite to PostgreSQL Data Migrator")
    parser.add_argument("--sqlite-path", default=os.path.join(os.path.dirname(__file__), "../../health_saathi.db"), help="Source SQLite database path")
    parser.add_argument("--target-url", default=None, help="Target PostgreSQL connection URL (defaults to DATABASE_URL in settings)")
    parser.add_argument("--dry-run", action="store_true", help="Simulate data migration without committing changes")
    parser.add_argument("--verify-only", action="store_true", help="Only verify row count parity and schema")

    args = parser.parse_args()

    target_url = args.target_url or settings.DATABASE_URL
    if not target_url or target_url.startswith("sqlite"):
        print("[WARNING] Target database is set to SQLite. Specify --target-url with a postgresql+psycopg:// connection string or configure DATABASE_URL in backend/.env.")
        if not args.verify_only and not args.dry_run:
            sys.exit(1)

    migrate_data(
        sqlite_path=os.path.abspath(args.sqlite_path),
        target_url=target_url,
        dry_run=args.dry_run,
        verify_only=args.verify_only
    )
