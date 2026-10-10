from datetime import date, timedelta
from typing import List, Dict, Any, Optional

class CyclePredictor:
    """
    Menstrual Cycle Analyzer with Cautious Variance Estimations.
    Never guarantees exact dates; highlights natural variability for PCOS.
    """
    
    @staticmethod
    def analyze_cycles(cycle_history: List[Dict[str, Any]]) -> Dict[str, Any]:
        if not cycle_history or len(cycle_history) == 0:
            return {
                "estimated_next_cycle": None,
                "variance_days": "Insufficient data (needs at least 1-2 logged cycles)",
                "phase_estimate": "Phase tracking active",
                "disclaimer": "Cycle tracking is for your awareness. PCOS menstrual intervals naturally vary."
            }
            
        # Sort by start_date ascending
        sorted_records = sorted(cycle_history, key=lambda x: str(x["start_date"]))
        latest = sorted_records[-1]
        
        # If dates are strings, parse them
        if isinstance(latest["start_date"], str):
            latest_start = date.fromisoformat(latest["start_date"])
        else:
            latest_start = latest["start_date"]
            
        today = date.today()
        days_since_latest = (today - latest_start).days
        
        # Average cycle length estimation (standard default: 32-35 days for PCOS monitoring)
        estimated_cycle_length = 33
        estimated_date = latest_start + timedelta(days=estimated_cycle_length)
        
        # Determine current estimated phase
        if days_since_latest <= 5:
            phase = "Menstrual Phase"
        elif days_since_latest <= 14:
            phase = "Follicular Phase"
        elif days_since_latest <= 18:
            phase = "Potential Ovulatory Window (Approximate)"
        elif days_since_latest <= 35:
            phase = "Luteal Phase"
        else:
            phase = "Delayed / Irregular Interval"
            
        return {
            "estimated_next_cycle": estimated_date.isoformat(),
            "variance_days": "± 5 to 8 days variance estimated",
            "phase_estimate": phase,
            "disclaimer": (
                "PCOS cycles frequently experience delayed ovulation. This range is a cautious estimate "
                "to help you plan, not a guaranteed calendar event."
            )
        }
