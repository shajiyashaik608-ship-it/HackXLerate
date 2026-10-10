"""
Deterministic safety guardrails and clinical warning detection for Health Saathi.

LIMITATION NOTICE:
This detector employs deterministic keyword matching and regular expressions to identify
high-risk clinical phrases. Keyword-based matching cannot comprehend clinical context,
subtle nuances, or all permutations of medical crises, and CANNOT replace triage by a
certified emergency physician or triage clinician.
"""

import re
from typing import Tuple, Optional, Dict, Any

EMERGENCY_DISCLAIMER_EN = (
    "🚨 URGENT MEDICAL ADVICE: The symptoms reported (such as severe pain, acute hemorrhage, "
    "or syncope/loss of consciousness) may require immediate emergency clinical attention. "
    "Please contact your local emergency services (112 in India, 911 in the US) or proceed to the "
    "nearest emergency department immediately. Do not delay emergency care for digital assistance."
)

EMERGENCY_DISCLAIMER_TE = (
    "🚨 అత్యవసర వైద్య సలహా: మీరు తెలిపిన లక్షణాలు (తీవ్రమైన కడుపు నొప్పి, విపరీతమైన రక్తస్రావం, "
    "లేదా స్పృహ తప్పడం వంటివి) తక్షణ అత్యవసర వైద్య పరీక్షలను కోరుతున్నాయి. "
    "దయచేసి ఆలస్యం చేయకుండా వెంటనే సమీపంలోని ఆసుపత్రి ఎమర్జెన్సీ విభాగాన్ని సంప్రదించండి "
    "లేదా 112 / 108 కు కాల్ చేయండి."
)

STANDARD_DISCLAIMER_EN = (
    "Educational health guidance only. Not a medical diagnosis, clinical prescription, or cure. "
    "Always discuss lab tests, prescriptions, and symptoms with your physician."
)

STANDARD_DISCLAIMER_TE = (
    "విద్యాపరమైన ఆరోగ్య సమాచారం మాత్రమే. ఇది రోగ నిర్ధారణ లేదా ప్రిస్క్రిప్షన్ కాదు. "
    "ఏదైనా సమస్య కోసం తప్పనిసరిగా మీ వైద్యుడిని సంప్రదించండి."
)

# Red-flag clinical emergency triggers (English and Telugu)
EMERGENCY_PATTERNS = [
    r"\b(severe|excruciating|unbearable|acute)\s+(pelvic|abdominal|stomach|lower belly)\s+pain\b",
    r"\b(heavy|soaking|gushing|severe|massive)\s+(bleeding|hemorrhage|blood loss)\b",
    r"\b(fainted|fainting|passed out|loss of consciousness|unconscious|blackout)\b",
    r"\b(chest pain|shortness of breath|difficulty breathing|cyanosis)\b",
    r"\b(soaking\s+(a\s+pad|two\s+pads)\s+an?\s+hour)\b",
    r"తీవ్రమైన\s+(కడుపు|పెల్విక్)\s+నొప్పి",
    r"అధిక\s+రక్తస్రావం",
    r"స్పృహ\s+(కోల్పోవడం|తప్పడం|లేకపోవడం)",
]

# Prohibited definitive diagnostic assertions or unsupported cure claims
PROHIBITED_CLAIMS = [
    r"\b(this will cure (your )?pcos)\b",
    r"\b(you definitely have pcos)\b",
    r"\b(stop taking your (metformin|birth control|medication))\b",
    r"\b(guaranteed cure for polycystic)\b",
    r"మీ\s+పిసిఒఎస్\s+పూర్తిగా\s+నయమవుతుంది",
]


def check_urgent_symptoms(text: str, language: str = "en") -> Tuple[bool, Optional[str]]:
    """
    Deterministically evaluates user query or symptom note for emergency red-flag indicators.
    Returns: (is_urgent, emergency_advice_message)
    """
    if not text:
        return False, None

    text_clean = text.lower()
    for pattern in EMERGENCY_PATTERNS:
        if re.search(pattern, text_clean, re.IGNORECASE):
            advice = EMERGENCY_DISCLAIMER_TE if language == "te" else EMERGENCY_DISCLAIMER_EN
            return True, advice

    return False, None


def sanitize_ai_output(text: str, language: str = "en") -> str:
    """
    Sanitizes AI model text to ensure no definitive diagnostic or cure claims are made.
    """
    sanitized = text
    for pattern in PROHIBITED_CLAIMS:
        if re.search(pattern, sanitized, re.IGNORECASE):
            sanitized = re.sub(
                pattern,
                "evidence-based lifestyle practices support overall hormonal well-being",
                sanitized,
                flags=re.IGNORECASE
            )

    return sanitized


def get_standard_safety_notice(language: str = "en") -> str:
    """Returns localized non-diagnostic safety disclaimer."""
    return STANDARD_DISCLAIMER_TE if language == "te" else STANDARD_DISCLAIMER_EN
