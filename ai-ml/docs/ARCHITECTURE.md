# 🏛️ Health Saathi System Architecture

Health Saathi is engineered as a privacy-centric personal health copilot featuring a modular two-layer architecture:
1. **Core Health Intelligence Layer**: Manages document parsing, longitudinal records, care reminders, and clinician consultation preparation.
2. **Specialized PCOS Companion Layer**: Delivers culturally relevant Indian nutrition guidance, menstrual tracking with cautious variability modeling, and bilingual Telugu/English educational assistance.

---

## 🔄 End-to-End Data Pipeline

```
[User Action: Document Upload / Voice Query / Symptom Log]
                       │
                       ▼
            [FastAPI Backend Gateway]
                       │
       ┌───────────────┼───────────────┐
       ▼               ▼               ▼
[Auth & Consent] [File Parser] [Safety Guardrails]
       │               │               │
       │               ▼               │
       │        [AI-ML Engines]        │
       │   • report_analyzer.py        │
       │   • food_recommender.py       │
       │   • cycle_predictor.py        │
       │   • telugu_assistant.py       │
       │   • doctor_summary_gen.py     │
       │               │               │
       └───────────────┼───────────────┘
                       │
                       ▼
          [Medical Safety Guardrails]
           (Blocks diagnostic claims,
            attaches ethical disclaimers,
            screens emergency red flags)
                       │
                       ▼
       [SQLAlchemy ORM -> PostgreSQL / SQLite]
                       │
                       ▼
          [Frontend: React 18 + Vite]
```

---

## 🛡️ Medical Safety & Ethical Boundaries
- **No Diagnostic Claims**: The system avoids definitive assertions such as *"You have PCOS"*. Instead, it categorizes parameters as standard or requiring clinician review.
- **Natural Cycle Variability**: Menstrual prediction provides realistic windows (e.g., ±5 to 8 days variance) rather than misleading exact timestamps.
- **Clinical Referral**: Flags emergency symptoms (e.g., severe pelvic pain, intense bleeding) for immediate in-person healthcare evaluation.
