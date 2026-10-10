# 🌿 Health Saathi — AI-Powered Personal Health Copilot
### Personalized Health Intelligence with Indian Nutrition & Telugu Voice PCOS Companion

> **Hackathon Edition**: Built for speed, clarity, and real-world medical accessibility. Designed with medical guardrails: strictly educational, no unsolicited diagnosis, and patient empowerment for clinical consultations.

---

## 📁 Project Architecture Overview

```text
hackathon/
├── frontend/             # React + Vite UI (Tailwind CSS, Voice, Interactive Dashboards)
├── backend/              # Python FastAPI REST API with Pydantic validation & JWT
├── ai-ml/                # Modular AI Engines: Report Analyzer, Indian Food Engine, Telugu Assistant
├── database/             # SQLAlchemy Models, DB initialization, and synthetic test seeds
├── tests/                # Pytest suites for API, health check, and medical safety guardrails
├── docs/                 # Complete architecture, API reference, and setup manuals
├── .env.example          # Environment variable template
├── .gitignore            # Git exclusion rules
└── README.md             # Project documentation
```

---

## 🚀 Quick Start Instructions

### 1. Backend Setup (FastAPI & Python 3.10+)
```bash
# Navigate to backend
cd backend

# Create and activate virtual environment
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Seed synthetic test database (demo user, sample reports, food items)
python ../database/seed_data.py

# Start FastAPI server
uvicorn app.main:app --reload --port 8000
```
API Documentation will be live at: `http://localhost:8000/docs`

### 2. Frontend Setup (React + Vite)
```bash
# In a new terminal, navigate to frontend
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```
Frontend will be live at: `http://localhost:5173`

---

## 🛡️ Medical Safety & Ethical Guidelines
- **Educational Only**: The AI explains terminology and normal ranges. It never issues diagnoses or treatment plans.
- **Doctor Preparation**: Aggregates patient notes into clean summaries for clinical consultations.
- **Uncertainty Principle**: Menstrual predictions show natural variance windows rather than deceptive exact dates.
