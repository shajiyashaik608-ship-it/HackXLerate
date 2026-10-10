import re
from typing import List, Dict, Any

CLINICAL_KNOWLEDGE_CORPUS = [
    {
        "id": "pcos_pathophysiology",
        "title": "International Evidence-based Guideline for the Assessment and Management of PCOS (Monash, 2023)",
        "keywords": ["pcos", "what is", "causes", "cysts", "ovaries", "follicles", "androgen", "etiology"],
        "content": (
            "PCOS is a complex endocrine condition diagnosed using the Rotterdam Criteria (requiring 2 of 3 features: "
            "irregular or absent ovulation, clinical/biochemical hyperandrogenism, and polycystic ovarian morphology on ultrasound, "
            "after excluding other conditions). It is strongly linked to insulin resistance and lifestyle factors."
        ),
        "source": "Monash University / ESHRE / ASRM Consensus Guidelines (2023)"
    },
    {
        "id": "insulin_resistance_lifestyle",
        "title": "Endocrine Society Clinical Practice Guidelines: PCOS and Metabolic Health",
        "keywords": ["insulin", "glucose", "metabolism", "weight", "acanthosis", "hba1c", "blood sugar", "metformin"],
        "content": (
            "Hyperinsulinemia directly stimulates the ovarian theca cells to synthesize excess androgens and suppresses "
            "Sex Hormone Binding Globulin (SHBG) production by the liver. Modulating insulin via high-fibre, low glycemic foods, "
            "physical activity, and sleep significantly improves ovulatory frequency."
        ),
        "source": "Endocrine Society Clinical Practice Guideline"
    },
    {
        "id": "indian_nutrition_pcos",
        "title": "ICMR-NIN Dietary Guidelines for Indians: Metabolic Wellness",
        "keywords": ["diet", "food", "nutrition", "carbs", "millets", "pesarattu", "dal", "protein", "rice", "methi", "flaxseed"],
        "content": (
            "Traditional Indian staples can be balanced by replacing refined polished rice and maida with whole grains "
            "(foxtail millet, ragi, jowar) and doubling pulse and green vegetable portions. Soluble fibres from fenugreek (methi) "
            "and whole legumes mitigate rapid glycemic spikes."
        ),
        "source": "ICMR - National Institute of Nutrition (NIN) Guidelines"
    },
    {
        "id": "cycle_irregularity",
        "title": "ACOG Practice Bulletin: Management of Abnormal Uterine Bleeding in Ovulatory Dysfunction",
        "keywords": ["period", "cycle", "irregular", "late", "amenorrhea", "oligomenorrhea", "bleeding", "flow"],
        "content": (
            "Infrequent menstrual cycles (oligomenorrhea, defined as cycles greater than 35 days apart) or absence of bleeding "
            "(amenorrhea) stem from chronic anovulation. Prolonged intervals between periods can cause unopposed estrogen stimulation "
            "on the endometrium, which requires periodic medical review."
        ),
        "source": "American College of Obstetricians and Gynecologists (ACOG)"
    },
    {
        "id": "laboratory_biomarkers",
        "title": "FOGSI Indian Consensus on Clinical & Biochemical PCOS Evaluation",
        "keywords": ["tsh", "lh", "fsh", "testosterone", "dhea", "fasting insulin", "thyroid", "test", "lab", "report"],
        "content": (
            "Essential laboratory evaluations include TSH and prolactin (to rule out primary thyroid disease or hyperprolactinemia), "
            "Total Testosterone and DHEA-S (for androgen excess), and fasting glucose/insulin. LH:FSH ratios above 2:1 are common "
            "correlates but not formal diagnostic requirements."
        ),
        "source": "Federation of Obstetric and Gynaecological Societies of India (FOGSI)"
    }
]


class RetrievalService:
    """
    Retrieves grounded clinical passages from curated health education guidelines.
    Never invents citations or medical recommendations.
    """

    def retrieve_relevant_passages(self, query: str, top_k: int = 2) -> List[Dict[str, Any]]:
        query_words = set(re.findall(r"\w+", query.lower()))
        scored_corpus = []

        for item in CLINICAL_KNOWLEDGE_CORPUS:
            score = 0
            # Keyword matching
            for kw in item["keywords"]:
                if kw in query.lower():
                    score += 3

            # Word overlap with content and title
            content_words = set(re.findall(r"\w+", item["content"].lower()))
            overlap = len(query_words.intersection(content_words))
            score += overlap

            if score > 0:
                scored_corpus.append((score, item))

        scored_corpus.sort(key=lambda x: x[0], reverse=True)
        return [item for _, item in scored_corpus[:top_k]]


retrieval_service = RetrievalService()
