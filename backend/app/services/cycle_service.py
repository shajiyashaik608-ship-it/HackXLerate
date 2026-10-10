from datetime import date, timedelta
from typing import List, Optional, Dict, Any
from collections import Counter
from sqlalchemy.orm import Session
from app.models.cycle import CycleRecord
from app.models.symptom import SymptomRecord
from app.repositories.cycle_repo import cycle_repo, symptom_repo
from app.repositories.user_repo import user_repo
from app.core.exceptions import NotFoundException, ValidationException
from app.utils.guardrails import check_urgent_symptoms


class CycleService:
    # ----------------- Menstrual Cycles -----------------

    def log_cycle(
        self,
        db: Session,
        user_id: int,
        start_date: date,
        end_date: Optional[date] = None,
        duration_days: Optional[int] = 4,
        flow_intensity: str = "medium",
        notes: Optional[str] = None
    ) -> CycleRecord:
        if end_date:
            if end_date < start_date:
                raise ValidationException("End date cannot precede the start date.")
            duration_days = (end_date - start_date).days + 1

        cycle = CycleRecord(
            user_id=user_id,
            start_date=start_date,
            end_date=end_date,
            duration_days=duration_days,
            flow_intensity=flow_intensity,
            notes=notes
        )
        return cycle_repo.create(db, cycle)

    def get_cycle_history(self, db: Session, user_id: int, skip: int = 0, limit: int = 50) -> List[CycleRecord]:
        return cycle_repo.get_by_user(db, user_id=user_id, skip=skip, limit=limit)

    def update_cycle(self, db: Session, cycle_id: int, user_id: int, update_data: dict) -> CycleRecord:
        cycle = cycle_repo.get_by_id_and_user(db, cycle_id=cycle_id, user_id=user_id)
        if not cycle:
            raise NotFoundException("Cycle entry not found.")

        start_date = update_data.get("start_date", cycle.start_date)
        end_date = update_data.get("end_date", cycle.end_date)
        if start_date and end_date and end_date < start_date:
            raise ValidationException("End date cannot precede start date.")

        if end_date and start_date:
            update_data["duration_days"] = (end_date - start_date).days + 1

        return cycle_repo.update(db, cycle, update_data)

    def delete_cycle(self, db: Session, cycle_id: int, user_id: int) -> bool:
        cycle = cycle_repo.get_by_id_and_user(db, cycle_id=cycle_id, user_id=user_id)
        if not cycle:
            raise NotFoundException("Cycle entry not found.")
        return cycle_repo.delete(db, cycle.id)

    def estimate_cycle(self, db: Session, user_id: int) -> Dict[str, Any]:
        """
        Calculates historical cycle intervals and returns a variance-aware interval estimate (±5 days).
        Never presents dates as exact calendar certainties.
        """
        cycles = cycle_repo.get_by_user(db, user_id=user_id, skip=0, limit=20)
        
        # Chronological order
        sorted_cycles = sorted(cycles, key=lambda c: c.start_date)

        intervals: List[int] = []
        if len(sorted_cycles) >= 2:
            for i in range(1, len(sorted_cycles)):
                diff_days = (sorted_cycles[i].start_date - sorted_cycles[i-1].start_date).days
                # Sanity filter (menstrual intervals between 15 and 180 days)
                if 15 <= diff_days <= 180:
                    intervals.append(diff_days)

        profile = user_repo.get_profile_by_user_id(db, user_id)
        baseline = profile.baseline_cycle_length if profile and profile.baseline_cycle_length else None

        has_sufficient_history = len(intervals) >= 2

        if has_sufficient_history:
            avg_interval = round(sum(intervals) / len(intervals), 1)
        elif baseline:
            avg_interval = float(baseline)
        else:
            avg_interval = 33.0  # Common clinical reference baseline for PCOS tracking

        if not sorted_cycles:
            return {
                "historical_intervals": [],
                "average_cycle_length": avg_interval,
                "estimation_method": "PCOS Adaptive Interval Heuristic (±5 Days)",
                "estimated_arrival_window": "Insufficient cycle history. Please log your most recent cycle start date.",
                "window_start": None,
                "window_end": None,
                "current_cycle_day": None,
                "phase_name": "No cycle recorded",
                "uncertainty_notice": "PCOS cycles exhibit natural biological variability. Dates are estimated windows rather than guaranteed exact days.",
                "has_sufficient_history": False
            }

        latest_cycle = sorted_cycles[-1]
        today = date.today()
        current_cycle_day = (today - latest_cycle.start_date).days + 1

        # Calculate estimated window (avg_interval ± 5 days)
        center_target = latest_cycle.start_date + timedelta(days=int(avg_interval))
        window_start = center_target - timedelta(days=5)
        window_end = center_target + timedelta(days=5)

        # Determine physiological phase heuristic
        if current_cycle_day <= (latest_cycle.duration_days or 5):
            phase_name = "Menstrual Phase"
        elif current_cycle_day <= 14:
            phase_name = "Follicular Phase"
        elif current_cycle_day <= 18:
            phase_name = "Approximate Ovulatory Window"
        elif current_cycle_day <= int(avg_interval):
            phase_name = "Luteal Phase"
        else:
            phase_name = "Extended / Variable Interval"

        window_str = f"{window_start.strftime('%b %d')} – {window_end.strftime('%b %d, %Y')}"

        return {
            "historical_intervals": intervals,
            "average_cycle_length": avg_interval,
            "estimation_method": "PCOS Adaptive Interval Heuristic (±5 Days)",
            "estimated_arrival_window": window_str,
            "window_start": window_start,
            "window_end": window_end,
            "current_cycle_day": max(1, current_cycle_day),
            "phase_name": phase_name,
            "uncertainty_notice": "PCOS cycles exhibit natural biological variability. Dates are estimated windows rather than guaranteed exact days.",
            "has_sufficient_history": has_sufficient_history
        }

    # ----------------- Symptom Records -----------------

    def log_symptom(
        self,
        db: Session,
        user_id: int,
        symptom_type: str,
        severity: str = "mild",
        recorded_date: Optional[date] = None,
        notes: Optional[str] = None
    ) -> SymptomRecord:
        symptom = SymptomRecord(
            user_id=user_id,
            recorded_date=recorded_date or date.today(),
            symptom_type=symptom_type.lower().strip(),
            severity=severity.lower().strip(),
            notes=notes
        )
        return symptom_repo.create(db, symptom)

    def get_symptom_history(
        self,
        db: Session,
        user_id: int,
        skip: int = 0,
        limit: int = 100,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None
    ) -> List[SymptomRecord]:
        return symptom_repo.get_by_user(
            db, user_id=user_id, skip=skip, limit=limit, start_date=start_date, end_date=end_date
        )

    def update_symptom(self, db: Session, symptom_id: int, user_id: int, update_data: dict) -> SymptomRecord:
        symptom = symptom_repo.get_by_id_and_user(db, symptom_id=symptom_id, user_id=user_id)
        if not symptom:
            raise NotFoundException("Symptom record not found.")
        return symptom_repo.update(db, symptom, update_data)

    def delete_symptom(self, db: Session, symptom_id: int, user_id: int) -> bool:
        symptom = symptom_repo.get_by_id_and_user(db, symptom_id=symptom_id, user_id=user_id)
        if not symptom:
            raise NotFoundException("Symptom record not found.")
        return symptom_repo.delete(db, symptom.id)

    def summarize_symptoms(self, db: Session, user_id: int) -> Dict[str, Any]:
        """
        Aggregates symptom frequencies and checks for urgent emergency triggers in notes.
        """
        records = symptom_repo.get_by_user(db, user_id=user_id, limit=200)

        urgent_flag = False
        urgent_message = None

        grouped: Dict[str, List[SymptomRecord]] = {}
        for rec in records:
            if rec.symptom_type not in grouped:
                grouped[rec.symptom_type] = []
            grouped[rec.symptom_type].append(rec)

            # Check for urgent signals in severe entries or notes
            if rec.severity == "severe" or (rec.notes and len(rec.notes) > 0):
                is_urgent, msg = check_urgent_symptoms(f"{rec.symptom_type} {rec.notes or ''}")
                if is_urgent:
                    urgent_flag = True
                    urgent_message = msg

        items = []
        for s_type, rec_list in grouped.items():
            severities = [r.severity for r in rec_list]
            most_common = Counter(severities).most_common(1)[0][0]
            latest_date = max(r.recorded_date for r in rec_list)
            items.append({
                "symptom_type": s_type,
                "count": len(rec_list),
                "most_common_severity": most_common,
                "last_reported_date": latest_date
            })

        items.sort(key=lambda x: x["count"], reverse=True)
        frequent = items[0]["symptom_type"] if items else None

        return {
            "total_entries": len(records),
            "symptoms": items,
            "frequent_symptom": frequent,
            "urgent_warning_flag": urgent_flag,
            "safety_message": urgent_message
        }


cycle_service = CycleService()
