import sys, os
import pytest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../backend")))
from app.utils.safety_guardrails import sanitize_and_validate_response

def test_guardrails_blocks_cure_claims():
    risky_input = "Drink cinnamon water and this will cure your pcos within 7 days."
    safe_text, escalate, warnings = sanitize_and_validate_response(risky_input, language="en")
    
    # Assert forbidden cure claim was eliminated or replaced
    assert "cure your pcos" not in safe_text.lower()
    assert "Disclaimer" in safe_text
    assert len(warnings) > 0

def test_guardrails_detects_emergency_red_flags():
    emergency_input = "I have severe pelvic pain and fainting since this morning."
    safe_text, escalate, warnings = sanitize_and_validate_response(emergency_input, language="en")
    
    assert escalate is True

def test_telugu_disclaimer_appended():
    telugu_input = "PCOS లో మంచి ఆహారపు అలవాట్లు పాటించాలి."
    safe_text, escalate, warnings = sanitize_and_validate_response(telugu_input, language="te")
    
    assert "గమనిక" in safe_text
