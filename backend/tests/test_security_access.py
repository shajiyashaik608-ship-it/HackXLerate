import pytest
from app.core.config import Settings
from app.models.document import MedicalDocument
from app.models.user import User
from app.core.security import get_password_hash, create_access_token


def test_unauthenticated_reports_upload_rejected(client):
    """Ensure report uploads require authentication and do not fall back to user 1."""
    res = client.post("/api/v1/reports/upload", files={"file": ("report.pdf", b"%PDF-1.4...", "application/pdf")})
    assert res.status_code == 401


def test_unauthenticated_reports_listing_rejected(client):
    """Ensure listing private medical reports requires authentication."""
    res = client.get("/api/v1/reports")
    assert res.status_code == 401


def test_unauthenticated_assistant_chat_rejected(client):
    """Ensure assistant conversations require authentication to prevent writing to user 1."""
    res = client.post("/api/v1/assistant/chat", json={"message": "Can you explain my reports?", "language": "en"})
    assert res.status_code == 401


def test_unauthenticated_doctor_prep_summary_rejected(client):
    """Ensure consultation summaries with private lab and cycle info require authentication."""
    res = client.get("/api/v1/doctor-prep/summary")
    assert res.status_code == 401


def test_cross_user_document_idor_rejected(client, db, test_user, auth_headers):
    """Ensure User B cannot access User A's uploaded documents."""
    # Create User B
    user_b = User(
        email="patient_b@healthsaathi.in",
        hashed_password=get_password_hash("OtherPass123!"),
        full_name="Patient B",
        is_active=True,
        is_verified=True,
        consent_given=True
    )
    db.add(user_b)
    db.commit()
    db.refresh(user_b)

    token_b = create_access_token({"sub": user_b.email, "user_id": user_b.id})
    headers_b = {"Authorization": f"Bearer {token_b}"}

    # Upload document owned by User A
    doc_a = MedicalDocument(
        user_id=test_user.id,
        file_name="patient_a_blood_panel.pdf",
        file_type="pdf",
        file_path="uploads/private/user_1/test.pdf",
        category="lab_report",
        processing_status="completed"
    )
    db.add(doc_a)
    db.commit()
    db.refresh(doc_a)

    # User A can view their own document
    res_a = client.get(f"/api/v1/reports/{doc_a.id}", headers=auth_headers)
    assert res_a.status_code == 200

    # User B attempting to view User A's document must receive 404 (prevent IDOR leakage)
    res_b = client.get(f"/api/v1/reports/{doc_a.id}", headers=headers_b)
    assert res_b.status_code == 404


def test_production_safety_validation():
    """Verify production safeguards reject insecure defaults and SQLite."""
    # Default development secret key rejected in production
    with pytest.raises(ValueError, match="SECRET_KEY must be set to a secure"):
        Settings(
            ENVIRONMENT="production",
            SECRET_KEY="development_secret_key_change_in_production_min_32_chars",
            DATABASE_URL="postgresql+psycopg://user:pass@host:5432/db"
        )

    # SQLite database rejected in production
    with pytest.raises(ValueError, match="Production requires a Supabase PostgreSQL"):
        Settings(
            ENVIRONMENT="production",
            SECRET_KEY="a_very_long_secure_custom_production_key_1234567890",
            DATABASE_URL="sqlite:///./health_saathi.db"
        )

    # Valid production settings disable DEMO_MODE automatically
    valid_prod = Settings(
        ENVIRONMENT="production",
        SECRET_KEY="a_very_long_secure_custom_production_key_1234567890",
        DATABASE_URL="postgresql+psycopg://user:pass@aws-0-ap-south-1.pooler.supabase.com:6543/postgres"
    )
    assert valid_prod.DEMO_MODE is False
    assert valid_prod.ENABLE_DEMO_SEED is False
