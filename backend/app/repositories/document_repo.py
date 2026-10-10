from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import select, desc
from app.repositories.base import BaseRepository
from app.models.document import MedicalDocument
from app.models.biomarker import Biomarker


class DocumentRepository(BaseRepository[MedicalDocument]):
    def __init__(self):
        super().__init__(MedicalDocument)

    def get_by_user(self, db: Session, user_id: int, skip: int = 0, limit: int = 50) -> List[MedicalDocument]:
        stmt = (
            select(MedicalDocument)
            .where(MedicalDocument.user_id == user_id)
            .order_by(desc(MedicalDocument.upload_date))
            .offset(skip)
            .limit(limit)
        )
        return list(db.scalars(stmt).all())

    def get_by_id_and_user(self, db: Session, document_id: int, user_id: int) -> Optional[MedicalDocument]:
        stmt = select(MedicalDocument).where(
            MedicalDocument.id == document_id,
            MedicalDocument.user_id == user_id
        )
        return db.scalars(stmt).first()


class BiomarkerRepository(BaseRepository[Biomarker]):
    def __init__(self):
        super().__init__(Biomarker)

    def get_by_user(self, db: Session, user_id: int, skip: int = 0, limit: int = 100) -> List[Biomarker]:
        stmt = (
            select(Biomarker)
            .where(Biomarker.user_id == user_id)
            .order_by(desc(Biomarker.test_date), desc(Biomarker.id))
            .offset(skip)
            .limit(limit)
        )
        return list(db.scalars(stmt).all())

    def get_by_document(self, db: Session, document_id: int, user_id: int) -> List[Biomarker]:
        stmt = (
            select(Biomarker)
            .where(Biomarker.document_id == document_id, Biomarker.user_id == user_id)
            .order_by(Biomarker.id)
        )
        return list(db.scalars(stmt).all())

    def get_by_id_and_user(self, db: Session, biomarker_id: int, user_id: int) -> Optional[Biomarker]:
        stmt = select(Biomarker).where(
            Biomarker.id == biomarker_id,
            Biomarker.user_id == user_id
        )
        return db.scalars(stmt).first()

    def get_trends(self, db: Session, user_id: int, test_name: Optional[str] = None) -> List[Biomarker]:
        stmt = select(Biomarker).where(Biomarker.user_id == user_id)
        if test_name:
            stmt = stmt.where(Biomarker.test_name.ilike(f"%{test_name}%"))
        stmt = stmt.order_by(Biomarker.test_date.asc(), Biomarker.id.asc())
        return list(db.scalars(stmt).all())


document_repo = DocumentRepository()
biomarker_repo = BiomarkerRepository()
