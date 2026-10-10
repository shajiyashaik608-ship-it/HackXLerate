import sys, os
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../ai-ml")))
from cycle_predictor import CyclePredictor

from app.database import get_db
from app.models.cycle_record import CycleRecord
from app.models.user import User
from app.schemas.cycle_record import CycleRecordCreate, CycleRecordResponse, CyclePredictionResponse
from app.api.deps import get_current_user

router = APIRouter(prefix="/cycle", tags=["Menstrual Cycle & Symptoms"])

@router.get("/", response_model=List[CycleRecordResponse])
def get_cycle_records(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return db.query(CycleRecord).filter(CycleRecord.user_id == current_user.id).order_by(CycleRecord.start_date.desc()).all()

@router.post("/log", response_model=CycleRecordResponse)
def log_cycle_event(payload: CycleRecordCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    record = CycleRecord(
        user_id=current_user.id,
        start_date=payload.start_date,
        end_date=payload.end_date,
        flow_intensity=payload.flow_intensity,
        symptoms=payload.symptoms,
        notes=payload.notes
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return record

@router.get("/prediction", response_model=CyclePredictionResponse)
def get_cautious_prediction(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    records = db.query(CycleRecord).filter(CycleRecord.user_id == current_user.id).order_by(CycleRecord.start_date.asc()).all()
    history_dicts = [
        {"start_date": r.start_date, "end_date": r.end_date, "flow_intensity": r.flow_intensity}
        for r in records
    ]
    return CyclePredictor.analyze_cycles(history_dicts)
