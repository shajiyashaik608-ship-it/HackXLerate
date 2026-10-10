# Health Saathi (PCOS Saathi) — Python Backend

Production-ready FastAPI backend for **Health Saathi (PCOS Saathi)**, an AI-powered personal health copilot focused on PCOS awareness, menstrual cycle tracking, laboratory report understanding, Indian nutrition, and healthcare appointment preparation.

---

## 1. Quick Start

### Prerequisites
* Python 3.11+
* (Optional) [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) for optical character recognition of scanned lab reports. (If not installed, fallback logic handles PDF embedded text and reports configuration state gracefully).

### Setup & Run

#### Windows PowerShell
```powershell
cd backend

# Create virtual environment
python -m venv .venv

# Activate virtual environment
.venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Copy environment template
Copy-Item .env.example .env

# Run Alembic migrations
alembic upgrade head

# Seed reproducible synthetic demo data
python -m app.db.init_db

# Start development server
uvicorn app.main:app --reload --port 8000
```

#### macOS / Linux
```bash
cd backend

# Create virtual environment
python3 -m venv .venv

# Activate virtual environment
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy environment template
cp .env.example .env

# Run Alembic migrations
alembic upgrade head

# Seed reproducible synthetic demo data
python3 -m app.db.init_db

# Start development server
uvicorn app.main:app --reload --port 8000
```

---

## 2. API Documentation & Swagger UI

Once running, interactive API docs are accessible at:
* Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
* ReDoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)
* Health Status: [http://localhost:8000/health](http://localhost:8000/health)
* Readiness Status: [http://localhost:8000/readiness](http://localhost:8000/readiness)

---

## 3. Pre-Seeded Synthetic Demo Account

Run `python -m app.db.init_db` to seed:
* **Demo Email**: `priya@healthsaathi.in`
* **Demo Password**: `Saathi@2026`
* **Pre-loaded Records**:
  - Sample Health Profile (26 yo, vegetarian, 35-day baseline)
  - 2 Sample Medical Reports with extracted TSH (4.8 mIU/L, flagged elevated), Fasting Insulin, LH, FSH, Testosterone
  - 4 Historical Menstrual Cycles with varying intervals (36d, 33d, 40d, 35d)
  - 3 Symptom Records (Cramps, Acne, Bloating)
  - 10 Authentic Regional Indian PCOS Meals (Pesarattu, Ragi Idli, Korralu, Kala Chana, etc.)
  - 3 Care Reminders (Myo-Inositol, Fenugreek hydration, Doctor appointment)
  - 4 Educational Community Peer Support Posts

---

## 4. Key Architectural Features

1. **Non-Diagnostic Medical Ethics**:
   - The AI assistant (`/api/v1/assistant/chat`) and biomarker explainers (`/api/v1/biomarkers/{id}/explain`) strictly provide educational context. They never assert definitive diagnoses or prescribe medications.
2. **Emergency Clinical Guardrails**:
   - `app/utils/guardrails.py` deterministically detects red-flag clinical crises (such as acute pelvic pain, excessive hemorrhage, or syncope) and returns immediate emergency referral messages without delaying for external AI calls.
3. **Adaptive Cycle Estimation**:
   - PCOS cycles naturally exhibit high variability. Cycle estimation uses historical start intervals and computes variance windows ($\mu \pm 5\text{ days}$) rather than false exact date predictions.
4. **Private Storage & Magic Byte Validation**:
   - Uploaded medical files are verified via true binary signatures (PDF `%PDF`, PNG `\x89PNG`, JPEG `\xff\xd8\xff`) and stored inside an isolated private folder (`./private_uploads/`), never exposed as public static files.
5. **Data Privacy & GDPR/HIPAA-Aligned Purge**:
   - `/api/v1/privacy/export`: Complete structured JSON export of all patient records.
   - `/api/v1/privacy/purge`: Requires explicit confirmation phrase (`DELETE MY HEALTH DATA`), wipes all database records across 13 tables, and securely deletes physical files.

---

## 5. Supabase PostgreSQL Configuration & Data Migration

Health Saathi supports Supabase PostgreSQL for high-scale, production deployments.

### Environment Setup
Update `backend/.env` with your Supabase credentials:
```env
# Transaction Pooler (Port 6543) - Application Runtime
DATABASE_URL="postgresql+psycopg://postgres.<project_ref>:[PASSWORD]@aws-0-ap-south-1.pooler.supabase.com:6543/postgres?pgbouncer=true"

# Session Pooler (Port 5432) - Direct / Alembic Migrations
DIRECT_URL="postgresql+psycopg://postgres.<project_ref>:[PASSWORD]@aws-0-ap-south-1.pooler.supabase.com:5432/postgres"

# JWT Authentication
JWT_SECRET_KEY="your-secure-random-secret-key-min-32-chars"
```

### Apply Schema Migrations
```powershell
alembic upgrade head
```

### Transfer Existing SQLite Data to Supabase
A safe, idempotent data migrator transfers existing records while maintaining foreign keys, timestamps, and sequence counters:
```powershell
# Dry run preview (no changes committed)
python app\db\migrate_sqlite_to_postgres.py --dry-run

# Execute data transfer
python app\db\migrate_sqlite_to_postgres.py

# Verify row counts and referential integrity
python app\db\migrate_sqlite_to_postgres.py --verify-only
```

---

## 6. Automated Tests

Run test suite:
```powershell
pytest -v
```
All tests run against an isolated test database with mocked external services.
