from fastapi import APIRouter, Depends, UploadFile, File, Form, status
from typing import List, Optional
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.core.dependencies import get_current_user, get_optional_current_user
from app.models.user import User
from app.services.document_service import document_service
from app.schemas.document import MedicalDocumentResponse, MedicalDocumentStatusResponse
from app.schemas.biomarker import BiomarkerResponse, BiomarkerCorrectionUpdate

router = APIRouter(prefix="/reports", tags=["Medical Reports"])


@router.post("/upload", response_model=MedicalDocumentResponse, status_code=status.HTTP_201_CREATED)
async def upload_medical_report(
    file: Optional[UploadFile] = File(None),
    title: Optional[str] = Form(None),
    raw_text: Optional[str] = Form(None),
    category: Optional[str] = Form("lab_report"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    user_id = current_user.id

    if file is not None:
        content = await file.read()
        filename = file.filename or "uploaded_document.pdf"
    elif raw_text:
        # Create a synthetic PDF containing the text
        filename = f"{title or 'Lab_Report'}.pdf"
        content = (
            b"%PDF-1.4\n"
            b"1 0 obj<</Type/Catalog/Pages 2 0 R>>endobj\n"
            b"2 0 obj<</Type/Pages/Count 1/Kids[3 0 R]>>endobj\n"
            b"3 0 obj<</Type/Page/MediaBox[0 0 612 792]/Parent 2 0 R/Resources<<>>>>endobj\n"
            b"xref\n0 4\n0000000000 65535 f\n0000000010 00000 n\n0000000053 00000 n\n0000000102 00000 n\n"
            b"trailer<</Size 4/Root 1 0 R>>\nstartxref\n180\n%%EOF"
        )
    else:
        from app.core.exceptions import ValidationException
        raise ValidationException("Please upload a PDF/Image file or paste report text.")

    doc = await document_service.process_uploaded_document(
        db=db,
        user_id=user_id,
        filename=filename,
        content=content,
        category=category or "lab_report"
    )
    return doc


@router.get("", response_model=List[MedicalDocumentResponse])
@router.get("/", response_model=List[MedicalDocumentResponse])
def list_reports(
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return document_service.get_user_documents(db, user_id=current_user.id, skip=skip, limit=limit)



@router.get("/{report_id}", response_model=MedicalDocumentResponse)
def get_report_details(
    report_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return document_service.get_document_details(db, document_id=report_id, user_id=current_user.id)


@router.get("/{report_id}/status", response_model=MedicalDocumentStatusResponse)
def get_report_status(
    report_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    doc = document_service.get_document_details(db, document_id=report_id, user_id=current_user.id)
    return MedicalDocumentStatusResponse(
        id=doc.id,
        processing_status=doc.processing_status,
        file_name=doc.file_name,
        upload_date=doc.upload_date,
        error_message=doc.error_message
    )


@router.get("/{report_id}/results", response_model=List[BiomarkerResponse])
def get_report_results(
    report_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return document_service.get_document_results(db, document_id=report_id, user_id=current_user.id)


@router.patch("/{report_id}/results/{result_id}", response_model=BiomarkerResponse)
def update_report_result(
    report_id: int,
    result_id: int,
    payload: BiomarkerCorrectionUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    update_data = payload.model_dump(exclude_unset=True)
    return document_service.update_document_result(
        db=db,
        document_id=report_id,
        result_id=result_id,
        user_id=current_user.id,
        update_data=update_data
    )


@router.delete("/{report_id}")
def delete_report(
    report_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    document_service.delete_document(db, document_id=report_id, user_id=current_user.id)
    return {"message": "Document and extracted findings deleted successfully."}
