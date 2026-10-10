import re
from typing import Tuple, List

STANDARD_DISCLAIMER_EN = (
    "Disclaimer: Health Saathi provides evidence-grounded educational information and care preparation. "
    "It is NOT a medical diagnostic tool and does not replace the professional judgment of a certified healthcare practitioner."
)

STANDARD_DISCLAIMER_TE = (
    "గమనిక: హెల్త్ సాథి అందించే సమాచారం కేవలం విద్యాపరమైన అవగాహన కోసం మాత్రమే. "
    "ఇది వైద్య నిర్ధారణ (diagnosis) కాదు. ఏదైనా ఆరోగ్య సమస్య కోసం తప్పనిసరిగా డాక్టర్‌ని సంప్రదించండి."
)

# Urgent red-flag symptoms requiring immediate clinical referral
RED_FLAG_PATTERNS = [
    r"severe (abdominal|pelvic) pain",
    r"sudden (heavy|excessive) bleeding",
    r"fainting|unconscious|dizziness with nausea",
    r"severe shortness of breath",
    r"తీవ్రమైన కడుపు నొప్పి",
    r"అధిక రక్తస్రావం",
    r"స్పృహ కోల్పోవడం"
]

def sanitize_and_validate_response(
    text: str, 
    language: str = "en"
) -> Tuple[str, bool, List[str]]:
    """
    Validates AI-generated response:
    1. Checks for forbidden definitive diagnostic phrases (e.g., 'You definitely have PCOS')
    2. Checks for unverified 'cure' claims
    3. Checks for emergency red flag indicators
    4. Appends appropriate bilingual educational disclaimer
    """
    disclaimer = STANDARD_DISCLAIMER_TE if language == "te" else STANDARD_DISCLAIMER_EN
    warnings = []
    
    # Strip forbidden claims if present
    forbidden_claims = [
        r"this will cure (your )?pcos",
        r"you have been diagnosed with pcos",
        r"stop taking your medication",
        r"మీ పిసిఒఎస్ పూర్తిగా తగ్గిపోతుంది"
    ]
    
    clean_text = text
    for pattern in forbidden_claims:
        if re.search(pattern, clean_text, re.IGNORECASE):
            warnings.append("Filtered absolute diagnostic or cure claim.")
            clean_text = re.sub(pattern, "this lifestyle practice supports healthy hormone balance", clean_text, flags=re.IGNORECASE)
            
    # Check for urgent symptoms
    escalate = False
    for red_flag in RED_FLAG_PATTERNS:
        if re.search(red_flag, clean_text, re.IGNORECASE):
            escalate = True
            break
            
    # Always ensure disclaimer is attached
    if disclaimer not in clean_text:
        clean_text = f"{clean_text}\n\n⚠️ {disclaimer}"
        
    return clean_text, escalate, warnings
