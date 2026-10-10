import re
from typing import Dict, Any, List
from app.utils.safety_guardrails import sanitize_and_validate_response

TELUGU_HEALTH_KNOWLEDGE = [
    {
        "keywords": ["pcos", "enti", "ante", "what is", "simple"],
        "answer_te": (
            "పిసిఒఎస్ (PCOS - Polycystic Ovary Syndrome) అనేది మహిళల్లో హార్మోన్ల అసమతుల్యత వల్ల వచ్చే సాధారణ జీవనశైలి సమస్య. "
            "దీనిలో అండాశయాలు (ovaries) ప్రతి నెలా సరిగ్గా అండం విడుదల చేయకపోవచ్చు. "
            "దీనివల్ల పీరియడ్స్ ఆలస్యం కావడం, ముఖంపై మొటిమలు, లేదా బరువు పెరగడం జరగవచ్చు. "
            "సరైన ఆహారం, వ్యాయామం, మరియు డాక్టర్ మార్గదర్శకత్వంతో దీనిని చక్కగా నియంత్రించవచ్చు."
        ),
        "answer_en": (
            "PCOS (Polycystic Ovary Syndrome) is a common hormonal condition where ovaries may not release an egg regularly. "
            "This can cause irregular menstrual cycles, acne, excess hair, or weight changes. "
            "It is manageable with balanced nutrition, regular movement, and clinician care."
        ),
        "sources": ["WHO Guidelines on PCOS", "FOGSI Indian Clinical Consensus"]
    },
    {
        "keywords": ["diet", "food", "tinali", "aaharam", "nutrition", "annam"],
        "answer_te": (
            "PCOS లో ఆహారం చాలా ముఖ్యం:\n"
            "1. పాలిష్ చేసిన తెల్ల బియ్యం బదులు కొర్రలు, రాగులు, జొన్నలు వాడండి.\n"
            "2. రోజూ పెసరట్టు, మొలకలు, లేదా గుడ్లు ద్వారా ప్రొటీన్ తీసుకోండి.\n"
            "3. మెంతులు, అవిసె గింజలు (flax seeds) ఇన్సులిన్ నియంత్రణకు సహాయపడతాయి.\n"
            "4. తీపి పదార్థాలు, బేకరీ వస్తువులు తగ్గించండి."
        ),
        "answer_en": (
            "Nutrition guidance for PCOS:\n"
            "1. Choose complex grains like millets, ragi, and jowar over refined white rice.\n"
            "2. Prioritize protein in every meal with moong dal, sprouts, paneer, or eggs.\n"
            "3. Fenugreek (methi) and flaxseeds support healthy insulin response.\n"
            "4. Minimize ultra-processed sweets and sugary beverages."
        ),
        "sources": ["ICMR Dietary Guidelines", "Endocrine Society Nutrition Protocol"]
    },
    {
        "keywords": ["doctor", "eppudu", "kalavali", "when to see", "irregular", "bleeding"],
        "answer_te": (
            "కింది పరిస్థితుల్లో తప్పనిసరిగా గైనకాలజిస్ట్‌ని సంప్రదించాలి:\n"
            "1. వరుసగా 3 నెలల కంటే ఎక్కువ కాలం పీరియడ్స్ రాకపోతే.\n"
            "2. తీవ్రమైన కడుపు నొప్పి లేదా విపరీతమైన రక్తస్రావం ఉంటే.\n"
            "3. గర్భధారణ కోసం ప్రయత్నిస్తూ సమస్యలు ఎదురవుతుంటే.\n"
            "మీరు డాక్టర్ వద్దకు వెళ్లేటప్పుడు మీ పీరియడ్స్ తేదీలు మరియు లక్షణాల వివరాలను తీసుకెళ్లండి."
        ),
        "answer_en": (
            "You should consult a gynecologist if:\n"
            "1. You have missed your period for over 3 consecutive months.\n"
            "2. You experience severe pelvic pain or heavy bleeding.\n"
            "3. You are planning a pregnancy and notice ovulatory irregularity.\n"
            "Carry a summary of your recent cycle dates and symptom notes to your appointment."
        ),
        "sources": ["ACOG Clinical Guidelines", "NHS Menstrual Health"]
    }
]

class TeluguAssistant:
    """
    Bilingual Telugu/English Health Education Assistant.
    Provides conversational, voice-ready health guidance.
    """
    
    @staticmethod
    def answer_query(query: str, language: str = "te") -> Dict[str, Any]:
        query_lower = query.lower()
        selected_knowledge = None
        
        # Check against reviewed knowledge bank
        for item in TELUGU_HEALTH_KNOWLEDGE:
            if any(k in query_lower for k in item["keywords"]):
                selected_knowledge = item
                break
                
        if selected_knowledge:
            raw_answer = selected_knowledge["answer_te"] if language == "te" else selected_knowledge["answer_en"]
            sources = selected_knowledge["sources"]
        else:
            # Contextual fallback response
            if language == "te":
                raw_answer = (
                    f"మీరు అడిగిన ప్రశ్న '{query}' గురించి:\n"
                    "PCOS లో ప్రతి ఒక్కరి లక్షణాలు వేరుగా ఉంటాయి. మీ ఆహారంలో పీచు పదార్థాలు (fibre), "
                    "మంచి ప్రొటీన్ ఉండేలా చూసుకోండి. సరైన రోగనిర్ధారణ కోసం మీ పరీక్షల రిపోర్టులను డాక్టర్‌తో చర్చించండి."
                )
            else:
                raw_answer = (
                    f"Regarding your query on '{query}':\n"
                    "PCOS affects each individual uniquely. Maintaining stable blood glucose through whole grains, "
                    "adequate protein, and daily gentle physical activity forms the foundation of lifestyle care. "
                    "Please discuss persistent symptoms with your clinician."
                )
            sources = ["ICMR Health Guidance"]
            
        # Run through safety guardrails
        safe_answer, escalate, _ = sanitize_and_validate_response(raw_answer, language=language)
        
        return {
            "answer": safe_answer,
            "language": language,
            "audio_text": safe_answer.split("⚠️")[0].strip(),
            "educational_sources": sources,
            "escalate_to_doctor": escalate
        }
