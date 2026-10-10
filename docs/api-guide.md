# Health Saathi API Guide & Reference

All endpoints are mounted under the prefix `/api/v1` unless indicated otherwise.

---

## 1. Endpoint Summary

| Module | Method | Endpoint | Description | Auth Required |
| :--- | :--- | :--- | :--- | :--- |
| **System** | `GET` | `/health` | Core health liveness check | No |
| **System** | `GET` | `/readiness` | Readiness status (DB, OCR, LLM) | No |
| **Auth** | `POST` | `/api/v1/auth/signup` | Register new user account | No |
| **Auth** | `POST` | `/api/v1/auth/login` | Login and obtain JWT tokens | No |
| **Auth** | `POST` | `/api/v1/auth/refresh` | Refresh access token | No |
| **Auth** | `POST` | `/api/v1/auth/logout` | Revoke user session | Yes |
| **Auth** | `GET` | `/api/v1/auth/me` | Current authenticated user | Yes |
| **Users** | `GET` | `/api/v1/users/me` | User profile & consent details | Yes |
| **Users** | `PATCH` | `/api/v1/users/settings` | Update account settings | Yes |
| **Users** | `POST` | `/api/v1/users/consent` | Update consent state | Yes |
| **Profile** | `GET` | `/api/v1/profile` | Get HealthProfile | Yes |
| **Profile** | `PATCH` | `/api/v1/profile` | Update HealthProfile | Yes |
| **Reports** | `POST` | `/api/v1/reports/upload` | Upload PDF/image report for OCR | Yes |
| **Reports** | `GET` | `/api/v1/reports` | List patient reports | Yes |
| **Reports** | `GET` | `/api/v1/reports/{id}` | Report status and metadata | Yes |
| **Reports** | `GET` | `/api/v1/reports/{id}/results` | Extracted lab biomarkers | Yes |
| **Reports** | `PATCH` | `/api/v1/reports/{id}/results/{res_id}` | Manually correct extracted value | Yes |
| **Reports** | `DELETE`| `/api/v1/reports/{id}` | Delete document and file | Yes |
| **Biomarkers**| `GET` | `/api/v1/biomarkers` | List all patient lab findings | Yes |
| **Biomarkers**| `GET` | `/api/v1/biomarkers/trends` | Grouped analyte trends over time | Yes |
| **Biomarkers**| `POST`| `/api/v1/biomarkers/{id}/explain`| Educational non-diagnostic explanation | Yes |
| **Biomarkers**| `PATCH`| `/api/v1/biomarkers/{id}` | Correct biomarker value | Yes |
| **Assistant** | `POST` | `/api/v1/assistant/chat` | Bilingual conversational copilot | Yes |
| **Assistant** | `GET` | `/api/v1/assistant/conversations` | Conversation history list | Yes |
| **Cycles** | `POST` | `/api/v1/cycles/log` | Log period start, end, and flow | Yes |
| **Cycles** | `GET` | `/api/v1/cycles/history` | Historical menstrual records | Yes |
| **Cycles** | `GET` | `/api/v1/cycles/estimate` | Adaptive variance-based cycle window | Yes |
| **Symptoms** | `POST` | `/api/v1/symptoms/log` | Record symptom and severity | Yes |
| **Symptoms** | `GET` | `/api/v1/symptoms/summary` | Aggregate symptom frequencies | Yes |
| **Nutrition** | `GET` | `/api/v1/nutrition/meals` | Filter Indian PCOS recipes | Yes |
| **Nutrition** | `GET` | `/api/v1/nutrition/recommend` | Daily breakfast/lunch/dinner plan | Yes |
| **Nutrition** | `POST` | `/api/v1/nutrition/plan` | Save daily meal plan | Yes |
| **Reminders** | `POST` | `/api/v1/reminders` | Create care reminder | Yes |
| **Reminders** | `POST` | `/api/v1/reminders/{id}/complete`| Mark reminder completed | Yes |
| **Reminders** | `POST` | `/api/v1/reminders/{id}/snooze` | Snooze reminder | Yes |
| **Consultation**|`POST`| `/api/v1/consultations/brief` | Synthesize doctor brief | Yes |
| **Dashboard** | `GET` | `/api/v1/dashboard/summary` | High-level clinical overview | Yes |
| **Timeline** | `GET` | `/api/v1/timeline` | Chronological health journey | Yes |
| **Community** | `GET` | `/api/v1/community/posts` | Browse peer support posts | No |
| **Community** | `POST` | `/api/v1/community/posts` | Post anonymously / with pseudonym | No / Yes |
| **Privacy** | `GET` | `/api/v1/privacy/export` | Complete structured JSON export | Yes |
| **Privacy** | `POST` | `/api/v1/privacy/purge` | Permanent data and account wipe | Yes |

---

## 2. Request & Response Examples

### 2.1 Authentication: Login
**Request:**
```http
POST /api/v1/auth/login HTTP/1.1
Content-Type: application/json

{
  "email": "priya@healthsaathi.in",
  "password": "Saathi@2026"
}
```

**Response (200 OK):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "email": "priya@healthsaathi.in",
    "full_name": "Priya Sharma (Synthetic Demo Profile)",
    "is_active": true,
    "is_verified": true,
    "consent_given": true,
    "created_at": "2026-10-10T00:00:00Z"
  }
}
```

---

### 2.2 Medical Report Upload & Biomarker Extraction
**Request:**
```http
POST /api/v1/reports/upload HTTP/1.1
Authorization: Bearer <TOKEN>
Content-Type: multipart/form-data

file: [Synthetic_Thyroid_Metabolic_Report.pdf]
category: "lab_report"
```

**Response (201 Created):**
```json
{
  "id": 1,
  "user_id": 1,
  "file_name": "Synthetic_Thyroid_Metabolic_Report.pdf",
  "file_type": "pdf",
  "category": "lab_report",
  "processing_status": "completed",
  "upload_date": "2026-10-10T00:00:00Z",
  "biomarkers": [
    {
      "id": 1,
      "test_name": "TSH",
      "observed_value": "4.8",
      "numeric_value": 4.8,
      "unit": "mIU/L",
      "reference_range_lower": 0.4,
      "reference_range_upper": 4.5,
      "reference_range_text": "0.4 - 4.5 mIU/L",
      "status": "elevated",
      "extraction_confidence": 0.95,
      "plain_explanation": "Thyroid Stimulating Hormone regulates metabolic rate and cycle timing.",
      "is_user_corrected": false
    }
  ]
}
```

---

### 2.3 Bilingual Assistant & Emergency Detection
**Standard Request (Telugu):**
```http
POST /api/v1/assistant/chat HTTP/1.1
Authorization: Bearer <TOKEN>
Content-Type: application/json

{
  "message": "పీసీఓఎస్ లో ఎలాంటి ఆహారం తీసుకోవాలి?",
  "language": "te"
}
```

**Response (200 OK):**
```json
{
  "conversation_id": 1,
  "answer": "PCOS లో భారతీయ పోషకాహార నియమాలు:\n• పాలిష్ చేసిన తెల్ల బియ్యం బదులుగా కొర్రలు, రాగులు, జొన్నలు వాడండి.\n• ప్రతి భోజనంలో పెసరట్టు, మొలకలు, పనీర్ ద్వారా మంచి ప్రొటీన్ ఉండేలా చూసుకోండి.\n• నానబెట్టిన మెంతులు మరియు అవిసె గింజలు ఇన్సులిన్ స్థాయిలను నియంత్రించడంలో సహాయపడతాయి.\n• స్వీట్లు, మైదా, శీతల పానీయాలు నివారించండి.\n\n⚠️ విద్యాపరమైన సమాచారం మాత్రమే. ఇది రోగ నిర్ధారణ కాదు.",
  "language": "te",
  "sources": [
    "ICMR - National Institute of Nutrition (NIN) Dietary Guidelines for Indians",
    "Endocrine Society Nutrition and PCOS Practice Guidelines"
  ],
  "safety_notice": "విద్యాపరమైన సమాచారం మాత్రమే. ఇది రోగ నిర్ధారణ కాదు.",
  "urgent_care_flag": false,
  "is_mock_response": true
}
```

**Emergency Symptom Request:**
```http
POST /api/v1/assistant/chat HTTP/1.1
Authorization: Bearer <TOKEN>
Content-Type: application/json

{
  "message": "I am experiencing severe pelvic pain and sudden heavy bleeding",
  "language": "en"
}
```

**Response (200 OK - Immediate Red-Flag Short-Circuit):**
```json
{
  "conversation_id": 0,
  "answer": "🚨 URGENT MEDICAL ADVICE: The symptoms reported (such as severe pain, acute hemorrhage, or syncope/loss of consciousness) may require immediate emergency clinical attention. Please contact your local emergency services (112 in India, 911 in the US) or proceed to the nearest emergency department immediately. Do not delay emergency care for digital assistance.",
  "language": "en",
  "sources": ["Emergency Medical Safety Protocol (112 Emergency Care)"],
  "safety_notice": "🚨 URGENT MEDICAL ADVICE...",
  "urgent_care_flag": true,
  "is_mock_response": false
}
```

---

### 2.4 Cycle Variance Estimation
**Request:**
```http
GET /api/v1/cycles/estimate HTTP/1.1
Authorization: Bearer <TOKEN>
```

**Response (200 OK):**
```json
{
  "historical_intervals": [37, 35, 37],
  "average_cycle_length": 36.3,
  "estimation_method": "PCOS Adaptive Interval Heuristic (±5 Days)",
  "estimated_arrival_window": "Nov 12 – Nov 22, 2026",
  "window_start": "2026-11-12",
  "window_end": "2026-11-22",
  "current_cycle_day": 16,
  "phase_name": "Approximate Ovulatory Window",
  "uncertainty_notice": "PCOS cycles exhibit natural biological variability. Dates are estimated windows rather than guaranteed exact days.",
  "has_sufficient_history": true
}
```

---

### 2.5 Privacy Purge
**Request:**
```http
POST /api/v1/privacy/purge HTTP/1.1
Authorization: Bearer <TOKEN>
Content-Type: application/json

{
  "confirm_phrase": "DELETE MY HEALTH DATA"
}
```

**Response (200 OK):**
```json
{
  "status": "completed",
  "message": "All personal health records, cycle entries, uploaded reports, and account data have been permanently deleted.",
  "records_deleted": {
    "physical_files": 2,
    "biomarkers": 5,
    "medical_documents": 2,
    "cycle_records": 4,
    "symptom_records": 3,
    "reminders": 3,
    "consultations": 1,
    "user": 1
  },
  "purged_at": "2026-10-10T00:30:00Z"
}
```
