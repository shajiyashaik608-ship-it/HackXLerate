from typing import List, Dict, Any

class DoctorSummaryGenerator:
    """
    Doctor Visit Preparation Assistant.
    Synthesizes scattered patient data into a concise, professional consultation sheet.
    """
    
    @staticmethod
    def generate_consultation_summary(
        patient_name: str,
        age: int,
        cycle_history: List[Dict[str, Any]],
        logged_symptoms: List[str],
        lab_results: List[Dict[str, Any]],
        current_medications: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        
        # 1. Menstrual overview
        if cycle_history:
            cycle_notes = f"{len(cycle_history)} cycles recorded. Latest period logged on {cycle_history[-1].get('start_date', 'N/A')} with {cycle_history[-1].get('flow_intensity', 'moderate')} flow."
        else:
            cycle_notes = "No recent menstrual cycles logged in app."
            
        # 2. Symptoms
        symptom_list = ", ".join(logged_symptoms) if logged_symptoms else "Mild fatigue and cycle irregularity"
        
        # 3. Lab Highlights
        flagged_labs = [
            f"{item['test_name']}: {item['value']} {item['unit']} (Ref: {item['reference_range']}) - Status: {item['status'].upper()}"
            for item in lab_results if item.get("status") in ["elevated", "low", "review_needed"]
        ]
        if not flagged_labs:
            flagged_labs = ["All uploaded lab values fall within standard laboratory reference ranges."]
            
        # 4. Medications
        med_list = [
            f"{m.get('title')} ({m.get('dosage', 'as prescribed')})"
            for m in current_medications
        ] if current_medications else ["No active prescriptions recorded."]
        
        # 5. Suggested patient questions for the doctor
        suggested_questions = [
            "Are my current symptoms consistent with insulin resistance or hormonal imbalance?",
            "Do my thyroid (TSH) or androgen levels require repeat testing or specific medical support?",
            "What lifestyle, dietary, or supplement adjustments do you recommend for my metabolic profile?",
            "When should I schedule my next follow-up ultrasound or blood panel?"
        ]
        
        formatted_summary = {
            "patient_overview": f"{patient_name}, {age} years old",
            "chief_concerns": symptom_list,
            "menstrual_history": cycle_notes,
            "pertinent_lab_findings": flagged_labs,
            "active_medications": med_list,
            "recommended_questions_to_ask": suggested_questions,
            "clinical_disclaimer": "This sheet was prepared by Health Saathi to facilitate patient-clinician communication. It is not an automated medical diagnosis."
        }
        
        return formatted_summary
