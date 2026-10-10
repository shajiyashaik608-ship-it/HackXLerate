# Health Saathi: Supabase PostgreSQL Integration Guide

This guide documents the enterprise-grade integration of **Supabase-hosted PostgreSQL** into **Health Saathi (PCOS Saathi)**, replacing the prototype development SQLite database while preserving application architecture, API contracts, and patient privacy.

---

## 1. Architectural Overview

Health Saathi uses SQLAlchemy 2 with the asynchronous-capable `psycopg` (v3) PostgreSQL driver to interface with Supabase's managed PostgreSQL infrastructure.

```
+-------------------------------------------------------------+
|               React 18 + Vite Frontend Client               |
+-------------------------------------------------------------+
                              |
                     REST API Calls (JWT Auth)
                              v
+-------------------------------------------------------------+
|                 FastAPI Application Server                  |
|    - SecurityHeadersMiddleware & CORS Restrictions          |
|    - JWT Authentication & RBAC Authorization                |
|    - Medical Document & OCR Pipeline                        |
+-------------------------------------------------------------+
         |                                           |
  Runtime Transactions                      Schema Migrations
(Port 6543, PgBouncer)                     (Port 5432, Session)
         v                                           v
+-------------------------------------------------------------+
|                      Supabase Pooler                        |
|   aws-0-ap-south-1.pooler.supabase.com                      |
+-------------------------------------------------------------+
                              |
                              v
+-------------------------------------------------------------+
|                  Supabase PostgreSQL Core                   |
|   - 18 Schema Tables with Referential Integrity             |
|   - Row Level Security (RLS) Active                         |
+-------------------------------------------------------------+
```

---

## 2. Supabase Connection Endpoints

Supabase provides two distinct endpoints via its connection pooler:

### A. Application Transaction-Mode Pooler (`DATABASE_URL`)
* **Endpoint:** `aws-0-ap-south-1.pooler.supabase.com:6543`
* **Mode:** Transaction pooling (`?pgbouncer=true`)
* **Use Case:** All standard runtime queries and API endpoints.
* **Driver Format:** `postgresql+psycopg://postgres.<project_ref>:[PASSWORD]@aws-0-ap-south-1.pooler.supabase.com:6543/postgres?pgbouncer=true`
* **Driver Optimization:** `prepare_threshold=None` is configured in SQLAlchemy connection arguments to disable psycopg3 prepared statement caching across pooled server connections.

### B. Migration Session-Mode Pooler (`DIRECT_URL`)
* **Endpoint:** `aws-0-ap-south-1.pooler.supabase.com:5432`
* **Mode:** Session pooling / Direct connection
* **Use Case:** Alembic schema migrations and DDL operations.
* **Driver Format:** `postgresql+psycopg://postgres.<project_ref>:[PASSWORD]@aws-0-ap-south-1.pooler.supabase.com:5432/postgres`

---

## 3. Environment Variables Configuration

Store credentials in `backend/.env`. Never commit secrets to version control.

### Required Environment Variables

| Variable Name | Description | Example Placeholder |
|---|---|---|
| `DATABASE_URL` | Runtime connection (transaction pooler) | `postgresql+psycopg://postgres.sgtcudpolarsobgldlmu:[PASSWORD]@aws-0-ap-south-1.pooler.supabase.com:6543/postgres?pgbouncer=true` |
| `DIRECT_URL` | Migration connection (session pooler) | `postgresql+psycopg://postgres.sgtcudpolarsobgldlmu:[PASSWORD]@aws-0-ap-south-1.pooler.supabase.com:5432/postgres` |
| `JWT_SECRET_KEY` | Secret key for HS256 JWT tokens (min 32 chars) | `openssl rand -hex 32` |
| `SECRET_KEY` | Fallback alias for JWT_SECRET_KEY | `openssl rand -hex 32` |
| `ENVIRONMENT` | Environment flag (`development` or `production`) | `development` / `production` |
| `DATABASE_POOL_SIZE` | SQLAlchemy connection pool size | `10` |
| `DATABASE_MAX_OVERFLOW`| Overflow connections allowed | `20` |
| `DATABASE_POOL_TIMEOUT` | Seconds to wait for pool connection | `30` |
| `DATABASE_POOL_RECYCLE` | Seconds before recycling connections | `1800` |

> **Important Password Encoding:** If your database password contains special characters (e.g., `#`, `@`, `:`, `/`, `%`, `?`), URL-encode the password using Python:
> ```powershell
> python -c "import urllib.parse; print(urllib.parse.quote_plus('your_password_here'))"
> ```

---

## 4. Execution Commands (Windows PowerShell)

### Step 1: Install Dependencies
```powershell
cd backend
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

### Step 2: Apply Alembic Migrations on PostgreSQL
Run schema migrations against the configured Supabase endpoint:
```powershell
alembic upgrade head
```

### Step 3: Transfer SQLite Data to Supabase PostgreSQL
Health Saathi includes an automated, idempotent migration utility that creates a backup and migrates all existing records:

```powershell
# Preview migration without modifying target (Dry Run)
python app\db\migrate_sqlite_to_postgres.py --dry-run

# Execute full transfer
python app\db\migrate_sqlite_to_postgres.py

# Verify row counts and foreign-key integrity after transfer
python app\db\migrate_sqlite_to_postgres.py --verify-only
```

### Step 4: Apply Supabase Row Level Security (RLS)
Execute `database/supabase_rls.sql` in the Supabase Dashboard SQL Editor to protect all 18 tables:
1. Open the Supabase Project Dashboard.
2. Navigate to **SQL Editor**.
3. Paste the contents of `database/supabase_rls.sql` and click **Run**.

### Step 5: Start Health Saathi Backend
```powershell
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

---

## 5. Security & Sensitive Health Data Architecture

Health Saathi implements defense-in-depth for sensitive women's reproductive health data:

1. **Authentication Enforcement:**
   - Every private health endpoint (`/api/v1/reports`, `/api/v1/reports/upload`, `/api/v1/assistant/chat`, `/api/v1/doctor-prep/summary`, `/api/v1/cycles`, `/api/v1/privacy/export`) strictly requires JWT authentication via `Depends(get_current_user)`.
   - The unauthenticated fallback to `user_id = 1` has been permanently removed.

2. **Insecure Direct Object Reference (IDOR) Prevention:**
   - Queries explicitly filter by `user_id == current_user.id` across documents, biomarkers, cycles, symptoms, and consultations.
   - Cross-user attempts to access medical documents return `404 Not Found` to prevent account enumeration.

3. **File Upload Hardening:**
   - Enforces 10MB maximum file size (`MAX_UPLOAD_SIZE_BYTES`).
   - Validates true binary signatures (magic bytes) for `%PDF`, `\x89PNG`, and `\xff\xd8\xff` JPEG.
   - Isolates uploads into user-specific private storage directories (`./uploads/private/user_{id}/`).

4. **Production Configuration Guardrails:**
   - In production (`ENVIRONMENT="production"`), the application automatically rejects default secret keys and completely blocks local SQLite execution.
   - Demo mode (`DEMO_MODE`) is strictly disabled in production.
