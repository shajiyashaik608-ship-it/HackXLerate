import re
import json
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
import httpx
from app.core.config import settings
from app.core.logging import logger


class BaseLLMProvider(ABC):
    @abstractmethod
    async def generate_response(
        self,
        prompt: str,
        system_instruction: str,
        context_passages: List[Dict[str, Any]],
        language: str = "en"
    ) -> Dict[str, Any]:
        """Generate grounded response returning answer, sources, and is_mock_response flag."""
        pass


class MockLLMProvider(BaseLLMProvider):
    """
    Clearly labelled offline demonstration provider.
    Delivers educational, grounded PCOS information without making external API calls.
    """

    CURATED_KNOWLEDGE = [
        {
            "keywords": ["pcos", "enti", "ante", "what is", "polycystic", "symptoms", "causes"],
            "answer_en": (
                "PCOS (Polycystic Ovary Syndrome) is a prevalent hormonal and metabolic condition characterized by ovulatory irregularity, "
                "elevated androgens (which may present as acne or facial hair), and characteristic ovarian ultrasound morphology.\n\n"
                "Key management pillars include:\n"
                "• Regulating insulin sensitivity via balanced complex carbohydrates\n"
                "• Regular restorative physical movement\n"
                "• Quality sleep and stress management\n"
                "• Collaborative clinician care for individualized treatment goals."
            ),
            "answer_te": (
                "పిసిఒఎస్ (PCOS - Polycystic Ovary Syndrome) అనేది మహిళల్లో హార్మోన్ల అసమతుల్యత వల్ల వచ్చే సాధారణ జీవనశైలి సమస్య.\n\n"
                "దీని ముఖ్య లక్షణాలు:\n"
                "• పీరియడ్స్ ఆలస్యం కావడం లేదా సక్రమంగా రాకపోవడం\n"
                "• ఇన్సులిన్ నిరోధకత వల్ల బరువు పెరగడం\n"
                "• ముఖంపై మొటిమలు లేదా అవాంఛిత రోమాలు రావడం\n\n"
                "కొర్రలు, రాగులు వంటి పోషకాహారం, నిత్య వ్యాయామం, మరియు డాక్టర్ పర్యవేక్షణతో దీనిని సమర్థవంతంగా నియంత్రించవచ్చు."
            ),
            "sources": [
                "WHO Fact Sheets: Polycystic Ovary Syndrome",
                "International Evidence-based Guideline for the Assessment and Management of PCOS (Monash, 2023)"
            ]
        },
        {
            "keywords": ["diet", "food", "tinali", "aaharam", "nutrition", "annam", "rice", "curry", "breakfast", "dinner"],
            "answer_en": (
                "For PCOS metabolic health in an Indian dietary context:\n"
                "• Replace high-glycemic polished white rice with whole millets (Foxtail millet / Korralu, Ragi, Jowar) or brown basmati.\n"
                "• Boost protein at every meal: Moong Dal Pesarattu, boiled Kala Chana, Paneer, or whole eggs.\n"
                "• Incorporate soluble fibre seeds: soaked methi (fenugreek) seeds and freshly ground flaxseeds.\n"
                "• Minimize deep-fried snacks, maida items, and sweetened beverages to keep postprandial glucose stable."
            ),
            "answer_te": (
                "PCOS లో భారతీయ పోషకాహార నియమాలు:\n"
                "• పాలిష్ చేసిన తెల్ల బియ్యం బదులుగా కొర్రలు, రాగులు, జొన్నలు వాడండి.\n"
                "• ప్రతి భోజనంలో పెసరట్టు, మొలకలు, పనీర్ లేదా గుడ్ల ద్వారా మంచి ప్రొటీన్ ఉండేలా చూసుకోండి.\n"
                "• నానబెట్టిన మెంతులు మరియు అవిసె గింజలు ఇన్సులిన్ స్థాయిలను నియంత్రించడంలో సహాయపడతాయి.\n"
                "• స్వీట్లు, మైదా, శీతల పానీయాలు మరియు వేపుళ్లు నివారించండి."
            ),
            "sources": [
                "ICMR - National Institute of Nutrition (NIN) Dietary Guidelines for Indians",
                "Endocrine Society Nutrition and PCOS Practice Guidelines"
            ]
        },
        {
            "keywords": ["tsh", "insulin", "lh", "fsh", "testosterone", "hba1c", "lab", "test", "report", "blood"],
            "answer_en": (
                "Regarding laboratory investigations in PCOS:\n"
                "• Fasting Insulin & HbA1c assess underlying glucose metabolism and insulin resistance.\n"
                "• LH and FSH ratio often reflects ovulatory signaling dynamics.\n"
                "• Total Testosterone and DHEA-S quantify androgen levels.\n"
                "• TSH rules out co-existing thyroid disorders that mimic menstrual irregularities.\n\n"
                "Notice: Laboratory reference ranges vary between individual testing machines and clinical labs. Always have a certified doctor interpret combined values in the context of your physical exam."
            ),
            "answer_te": (
                "ల్యాబ్ పరీక్షల ఫలితాల గురించి ప్రాథమిక అవగాహన:\n"
                "• TSH పరీక్ష థైరాయిడ్ సమస్యలను నిర్ధారించడానికి ఉపయోగపడుతుంది.\n"
                "• ఫాస్టింగ్ ఇన్సులిన్ మరియు HbA1c శరీరంలో గ్లూకోజ్ నియంత్రణను సూచిస్తాయి.\n"
                "• LH / FSH మరియు టెస్టోస్టెరాన్ హార్మోన్ల స్థాయిలను తెలియజేస్తాయి.\n\n"
                "గమనిక: ల్యాబ్ మిషన్లను బట్టి నార్మల్ రేంజ్‌లు మారుతుంటాయి. పూర్తి విశ్లేషణ కోసం మీ డాక్టర్‌ను సంప్రదించండి."
            ),
            "sources": [
                "American Association of Clinical Endocrinologists (AACE)",
                "FOGSI Consensus on PCOS Investigations"
            ]
        },
        {
            "keywords": ["doctor", "eppudu", "kalavali", "when to see", "consult", "questions", "appointment"],
            "answer_en": (
                "When preparing for your clinician visit, consider bringing up:\n"
                "1. 'What specific phenotype or metabolic markers are most relevant to my presentation?'\n"
                "2. 'Should we monitor lipid profiles and 2-hour oral glucose tolerance?'\n"
                "3. 'What target interval between periods should we aim for to safeguard endometrial health?'\n"
                "4. 'Are lifestyle modifications sufficient right now or is medical therapy indicated?'"
            ),
            "answer_te": (
                "మీ డాక్టర్‌ను అడగవలసిన ముఖ్యమైన ప్రశ్నలు:\n"
                "1. 'నా లక్షణాలను బట్టి ఏ పరీక్షలు చేయించుకోవాలి?'\n"
                "2. 'పీరియడ్స్ క్రమబద్ధీకరించడానికి జీవనశైలి మార్పులు సరిపోతాయా?'\n"
                "3. 'నా ఇన్సులిన్ స్థాయిలను ఎలా ట్రాక్ చేయాలి?'\n"
                "డాక్టర్ దగ్గరకు వెళ్లేటప్పుడు మీ పీరియడ్స్ తేదీలు మరియు లక్షణాల వివరాలను తీసుకెళ్లండి."
            ),
            "sources": [
                "NHS Clinical Care Guidelines",
                "ACOG Patient Education: PCOS"
            ]
        }
    ]

    async def generate_response(
        self,
        prompt: str,
        system_instruction: str,
        context_passages: List[Dict[str, Any]],
        language: str = "en"
    ) -> Dict[str, Any]:
        prompt_lower = prompt.lower()
        matched_item = None

        for item in self.CURATED_KNOWLEDGE:
            if any(k in prompt_lower for k in item["keywords"]):
                matched_item = item
                break

        if matched_item:
            answer = matched_item["answer_te"] if language == "te" else matched_item["answer_en"]
            sources = matched_item["sources"]
        else:
            if language == "te":
                answer = (
                    f"మీరు అడిగిన విషయం '{prompt}' పై విశ్లేషణ:\n\n"
                    "PCOS లో ప్రతి ఒక్కరి హార్మోన్ స్థాయిలు మరియు లక్షణాలు భిన్నంగా ఉంటాయి. "
                    "తగినంత పీచు పదార్థాలు (fibre), సంపూర్ణ ధాన్యాలు, మరియు క్రమం తప్పని వ్యాయామం ద్వారా ఆరోగ్యాన్ని మెరుగుపరచుకోవచ్చు. "
                    "వ్యక్తిగత చికిత్స లేదా అనుమానాల కోసం దయచేసి అర్హత కలిగిన వైద్యులను సంప్రదించండి."
                )
            else:
                answer = (
                    f"Regarding your inquiry on '{prompt}':\n\n"
                    "PCOS is a heterogeneous condition where hormonal, metabolic, and lifestyle factors interact uniquely for each person. "
                    "Foundational care emphasizes whole foods with low glycemic impact, consistent movement, and restorative sleep. "
                    "For specific diagnostic evaluation and prescription management, please consult your physician."
                )
            sources = [
                "ICMR Dietary Guidelines for Indians",
                "International PCOS Guideline (Monash University, 2023)"
            ]

        # Add context from retrieved passages if available
        if context_passages:
            context_snippet = "\n\nReferenced knowledge notes: " + ", ".join([p.get("title", "") for p in context_passages if "title" in p])
            answer += context_snippet

        return {
            "answer": answer,
            "language": language,
            "sources": sources,
            "is_mock_response": True
        }


class GeminiLLMProvider(BaseLLMProvider):
    """
    Google Gemini Provider for real AI generation with automatic fallback to Mock provider.
    """
    def __init__(self, api_key: str, model_name: str = "gemini-1.5-flash"):
        self.api_key = api_key
        self.model_name = model_name
        self.fallback_mock = MockLLMProvider()

    async def generate_response(
        self,
        prompt: str,
        system_instruction: str,
        context_passages: List[Dict[str, Any]],
        language: str = "en"
    ) -> Dict[str, Any]:
        if not self.api_key or self.api_key == "mock-key":
            return await self.fallback_mock.generate_response(prompt, system_instruction, context_passages, language)

        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model_name}:generateContent?key={self.api_key}"
            
            # Format context
            context_text = "\n\n".join([f"Source ({p.get('title', 'Ref')}): {p.get('content', '')}" for p in context_passages])
            full_prompt = (
                f"{system_instruction}\n\n"
                f"Target Language: {'Telugu' if language == 'te' else 'English'}\n\n"
                f"Curated Health Knowledge:\n{context_text}\n\n"
                f"User Question: {prompt}\n\n"
                f"Remember: Do not diagnose. Do not prescribe. Ground explanations in the provided knowledge."
            )

            payload = {
                "contents": [{"parts": [{"text": full_prompt}]}],
                "generationConfig": {
                    "temperature": 0.2,
                    "maxOutputTokens": 800
                }
            }

            async with httpx.AsyncClient(timeout=10.0) as client:
                res = await client.post(url, json=payload)
                if res.status_code == 200:
                    data = res.json()
                    candidates = data.get("candidates", [])
                    if candidates and "content" in candidates[0]:
                        parts = candidates[0]["content"].get("parts", [])
                        if parts and "text" in parts[0]:
                            text_out = parts[0]["text"]
                            sources = [p.get("title", "Clinical Consensus") for p in context_passages] or ["International Evidence-based PCOS Guidelines"]
                            return {
                                "answer": text_out,
                                "language": language,
                                "sources": sources,
                                "is_mock_response": False
                            }
                logger.warning(f"Gemini API returned status {res.status_code}, falling back to mock provider.")
        except Exception as e:
            logger.error(f"Error calling Gemini LLM: {str(e)}. Falling back to mock provider.")

        return await self.fallback_mock.generate_response(prompt, system_instruction, context_passages, language)


def get_llm_provider() -> BaseLLMProvider:
    """Factory returns configured LLM provider or Mock provider based on environment."""
    if settings.LLM_PROVIDER.lower() == "gemini" and settings.GEMINI_API_KEY and settings.GEMINI_API_KEY != "mock-key":
        return GeminiLLMProvider(api_key=settings.GEMINI_API_KEY, model_name=settings.LLM_MODEL)
    return MockLLMProvider()
