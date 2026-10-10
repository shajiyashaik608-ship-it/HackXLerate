from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from app.models.document import MedicalDocument
from app.models.biomarker import Biomarker
from app.repositories.document_repo import document_repo, biomarker_repo
from app.integrations.storage_provider import storage_provider
from app.services.ocr_service import ocr_service
from app.services.extraction_service import extraction_service
from app.core.exceptions import NotFoundException, ValidationException
from app.core.logging import logger


class DocumentService:
    async def process_uploaded_document(
        self,
        db: Session,
        user_id: int,
        filename: str,
        content: bytes,
        category: str = "lab_report"
    ) -> MedicalDocument:
        """
        Validates, saves, OCRs, extracts biomarkers, and records results.
        """
        # 1. Save file in private storage
        file_path, file_type = await storage_provider.save_file(
            user_id=user_id,
            original_filename=filename,
            content=content
        )

        # 2. Create initial DB document record
        doc = MedicalDocument(
            user_id=user_id,
            file_name=filename,
            file_type=file_type,
            file_path=file_path,
            category=category,
            processing_status="processing"
        )
        db.add(doc)
        db.commit()
        db.refresh(doc)

        try:
            # 3. Extract text via OCR service
            extracted_text, pages_data, ocr_meta = ocr_service.extract_text_from_document(
                file_bytes=content,
                file_type=file_type
            )
            doc.ocr_raw_text = extracted_text

            if not extracted_text:
                doc.processing_status = "needs_review"
                doc.error_message = "No readable text could be recognized. Please review or upload a clearer document."
                db.commit()
                db.refresh(doc)
                return doc

            # 4. Extract biomarkers
            extracted_biomarkers = extraction_service.extract_biomarkers(pages_data)

            if extracted_biomarkers:
                has_uncertain = False
                for b_data in extracted_biomarkers:
                    biomarker = Biomarker(
                        user_id=user_id,
                        document_id=doc.id,
                        test_name=b_data["test_name"],
                        observed_value=b_data["observed_value"],
                        numeric_value=b_data["numeric_value"],
                        unit=b_data["unit"],
                        reference_range_lower=b_data["reference_range_lower"],
                        reference_range_upper=b_data["reference_range_upper"],
                        reference_range_text=b_data["reference_range_text"],
                        status=b_data["status"],
                        test_date=b_data["test_date"],
                        extraction_confidence=b_data["extraction_confidence"],
                        source_page=b_data["source_page"],
                        plain_explanation=b_data["plain_explanation"],
                        is_user_corrected=False
                    )
                    db.add(biomarker)
                    if b_data["status"] == "needs_review" or b_data["extraction_confidence"] < 0.8:
                        has_uncertain = True

                doc.processing_status = "needs_review" if has_uncertain else "completed"
            else:
                doc.processing_status = "needs_review"
                doc.error_message = "Document analyzed, but standard PCOS metabolic tests were not detected automatically."

            db.commit()
            db.refresh(doc)
            return doc

        except Exception as e:
            logger.error(f"Processing failed for document {doc.id}: {str(e)}")
            doc.processing_status = "failed"
            doc.error_message = "Document processing encountered an unexpected error."
            db.commit()
            db.refresh(doc)
            return doc

    def get_user_documents(self, db: Session, user_id: int, skip: int = 0, limit: int = 50) -> List[MedicalDocument]:
        return document_repo.get_by_user(db, user_id=user_id, skip=skip, limit=limit)

    def get_document_details(self, db: Session, document_id: int, user_id: int) -> MedicalDocument:
        doc = document_repo.get_by_id_and_user(db, document_id=document_id, user_id=user_id)
        if not doc:
            raise NotFoundException("Medical report not found.")
        return doc

    def get_document_results(self, db: Session, document_id: int, user_id: int) -> List[Biomarker]:
        self.get_document_details(db, document_id=document_id, user_id=user_id)
        return biomarker_repo.get_by_document(db, document_id=document_id, user_id=user_id)

    def update_document_result(
        self,
        db: Session,
        document_id: int,
        result_id: int,
        user_id: int,
        update_data: dict
    ) -> Biomarker:
        self.get_document_details(db, document_id=document_id, user_id=user_id)
        biomarker = biomarker_repo.get_by_id_and_user(db, biomarker_id=result_id, user_id=user_id)
        if not biomarker or biomarker.document_id != document_id:
            raise NotFoundException("Biomarker result not found.")

        # Apply corrections
        for field, val in update_data.items():
            if hasattr(biomarker, field) and val is not None:
                setattr(biomarker, field, val)

        # Recalculate status if range or numeric value changed
        if biomarker.numeric_value is not None and biomarker.reference_range_lower is not None and biomarker.reference_range_upper is not None:
            if biomarker.numeric_value < biomarker.reference_range_lower:
                biomarker.status = "low"
            elif biomarker.numeric_value > biomarker.reference_range_upper:
                biomarker.status = "elevated"
            else:
                biomarker.status = "normal"

        biomarker.is_user_corrected = True
        db.commit()
        db.refresh(biomarker)
        return biomarker

    def delete_document(self, db: Session, document_id: int, user_id: int) -> bool:
        doc = self.get_document_details(db, document_id=document_id, user_id=user_id)
        # 1. Remove physical file
        if doc.file_path:
            storage_provider.delete_file(doc.file_path)

        # 2. Delete DB record (cascade deletes biomarkers)
        db.delete(doc)
        db.commit()
        return True


document_service = DocumentService()
