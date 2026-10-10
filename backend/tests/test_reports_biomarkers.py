import io
from app.models.document import MedicalDocument
from app.models.biomarker import Biomarker


def test_upload_invalid_file_rejected(client, auth_headers):
    # Missing magic bytes / invalid extension
    corrupt_bytes = b"This is not a real PDF"
    files = {"file": ("malicious.exe", corrupt_bytes, "application/octet-stream")}
    res = client.post("/api/v1/reports/upload", files=files, headers=auth_headers)
    assert res.status_code in [400, 422]


def test_upload_valid_pdf_and_view(client, auth_headers, other_auth_headers):
    # Minimal valid PDF structure with %PDF header
    valid_pdf_content = (
        b"%PDF-1.4\n"
        b"1 0 obj<</Type/Catalog/Pages 2 0 R>>endobj\n"
        b"2 0 obj<</Type/Pages/Count 1/Kids[3 0 R]>>endobj\n"
        b"3 0 obj<</Type/Page/MediaBox[0 0 612 792]/Parent 2 0 R/Resources<<>>>>endobj\n"
        b"xref\n0 4\n0000000000 65535 f\n0000000010 00000 n\n0000000053 00000 n\n0000000102 00000 n\n"
        b"trailer<</Size 4/Root 1 0 R>>\nstartxref\n180\n%%EOF"
    )

    files = {"file": ("report_test.pdf", valid_pdf_content, "application/pdf")}
    res = client.post("/api/v1/reports/upload", files=files, headers=auth_headers)
    assert res.status_code == 201
    doc_id = res.json()["id"]

    # Current user can fetch report
    get_res = client.get(f"/api/v1/reports/{doc_id}", headers=auth_headers)
    assert get_res.status_code == 200

    # Cross-user access rejected (404)
    cross_res = client.get(f"/api/v1/reports/{doc_id}", headers=other_auth_headers)
    assert cross_res.status_code == 404


def test_biomarker_crud_and_explain(client, db, test_user, auth_headers):
    # Create biomarker in DB
    bio = Biomarker(
        user_id=test_user.id,
        test_name="TSH",
        observed_value="5.2",
        numeric_value=5.2,
        unit="mIU/L",
        reference_range_lower=0.4,
        reference_range_upper=4.5,
        reference_range_text="0.4 - 4.5 mIU/L",
        status="elevated",
        extraction_confidence=0.95,
        plain_explanation="Thyroid test"
    )
    db.add(bio)
    db.commit()
    db.refresh(bio)

    # List biomarkers
    list_res = client.get("/api/v1/biomarkers", headers=auth_headers)
    assert list_res.status_code == 200
    assert len(list_res.json()) >= 1

    # Explain biomarker
    exp_res = client.post(f"/api/v1/biomarkers/{bio.id}/explain", headers=auth_headers)
    assert exp_res.status_code == 200
    assert "explanation" in exp_res.json()
    assert "suggested_questions" in exp_res.json()

    # Manual correction
    patch_res = client.patch(
        f"/api/v1/biomarkers/{bio.id}",
        json={"observed_value": "4.2", "numeric_value": 4.2},
        headers=auth_headers
    )
    assert patch_res.status_code == 200
    assert patch_res.json()["status"] == "normal"
    assert patch_res.json()["is_user_corrected"] is True

    # Trends
    trend_res = client.get("/api/v1/biomarkers/trends", headers=auth_headers)
    assert trend_res.status_code == 200
    assert "trends" in trend_res.json()
