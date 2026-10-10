import sys, os
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../ai-ml")))
from doctor_summary_generator import DoctorSummaryGenerator

from app.database import get_db
from app.models.user import User
from app.models.cycle_record import CycleRecord
from app.models.medical_report import MedicalReport
from app.models.reminder import Reminder
from app.api.deps import get_current_user

router = APIRouter(prefix="/doctor-prep", tags=["Doctor Visit Prep"])

@router.get("/summary")
def get_consultation_summary(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # Fetch user's cycle records
    cycles = db.query(CycleRecord).filter(CycleRecord.user_id == current_user.id).order_by(CycleRecord.start_date.asc()).all()
    cycle_history = [{"start_date": c.start_date.isoformat(), "flow_intensity": c.flow_intensity} for c in cycles]
    
    # Collect logged symptoms
    symptom_set = set()
    for c in cycles:
        if c.symptoms:
            for s in c.symptoms:
                symptom_set.add(s)
                
    # Fetch latest reports & biomarkers
    reports = db.query(MedicalReport).filter(MedicalReport.user_id == current_user.id).all()
    all_biomarkers = []
    for r in reports:
        if r.structured_data:
            all_biomarkers.extend(r.structured_data)
            
    # Fetch medications
    meds = db.query(Reminder).filter(Reminder.user_id == current_user.id, Reminder.reminder_type == "medication").all()
    med_list = [{"title": m.title, "dosage": m.dosage} for m in meds]
    
    summary = DoctorSummaryGenerator.generate_consultation_summary(
        patient_name=current_user.full_name,
        age=24,
        cycle_history=cycle_history,
        logged_symptoms=list(symptom_set),
        lab_results=all_biomarkers,
        current_medications=med_list
    )
    return summary
