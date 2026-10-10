# 📖 Health Saathi REST API Reference

Base URL: `http://localhost:8000/api/v1`

---

## 1. System Health
### `GET /health`
Returns system status and active guardrail indicators.

---

## 2. Authentication
### `POST /api/v1/auth/signup`
Creates a user profile with consent and preferred language.
- **Body**: `{ "email": "user@example.com", "password": "...", "full_name": "...", "preferred_language": "te" }`

### `POST /api/v1/auth/login`
Returns a JWT access token.
- **Body**: `{ "email": "user@example.com", "password": "..." }`

---

## 3. Medical Report Intelligence
### `GET /api/v1/reports/`
Returns all chronological medical records for the authenticated user.

### `POST /api/v1/reports/upload`
Uploads a PDF/Image or submits lab text. Triggers `ReportAnalyzer` for biomarker extraction and generates plain-language explanations.

---

## 4. Indian PCOS Food Companion
### `GET /api/v1/food/recommendations`
Query parameters:
- `diet_type`: `vegetarian`, `non_vegetarian`, `eggitarian`
- `meal_type`: `breakfast`, `lunch`, `dinner`, `snack`
- `budget_friendly`: `true` or `false`

---

## 5. PCOS Saathi (Telugu & English Assistant)
### `POST /api/v1/assistant/chat`
- **Body**: `{ "question": "PCOS ante enti?", "language": "te" }`
- **Returns**: Evidence-based answer, audio playback text, citation sources, and attached clinical disclaimers.

---

## 6. Doctor Visit Prep
### `GET /api/v1/doctor-prep/summary`
Synthesizes logged menstrual records, symptom logs, active medications, and abnormal lab biomarkers into a clean 1-page clinical brief.

---

## 7. Cycle & Symptom Tracking
### `GET /api/v1/cycle/`
Fetches user menstrual history.

### `POST /api/v1/cycle/log`
Logs period start/end dates, flow intensity, and symptom tags.

### `GET /api/v1/cycle/prediction`
Returns cautious phase and interval estimates with variance windows.
