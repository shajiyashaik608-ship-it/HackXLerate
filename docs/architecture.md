# Health Saathi (PCOS Saathi) — System Architecture

## 1. Executive Summary

**Health Saathi (PCOS Saathi)** is an AI-powered Personal Health Copilot engineered specifically for women navigating Polycystic Ovary Syndrome (PCOS). The system bridges clinical complexity, cultural Indian dietary realities, and patient self-advocacy through non-diagnostic educational guidance, laboratory report analysis, adaptive menstrual cycle variance estimation, and doctor visit preparation.

---

## 2. Layered Architecture

```mermaid
graph TD
    Client["React 18 + Vite Frontend<br/>(Preserved Client App)"]
    
    subgraph FastAPI_Backend ["FastAPI Application (Port 8000)"]
        direction TB
        MW["SecurityHeadersMiddleware<br/>CORS / X-Request-ID"]
        Router["Master API Router (/api/v1)"]
        
        subgraph APISubmodules ["Domain Routers"]
            AuthR["auth.py & users.py"]
            ReportR["reports.py & biomarkers.py"]
            AssistR["assistant.py"]
            CycleR["cycles.py & symptoms.py"]
            NutriR["nutrition.py"]
            CareR["reminders.py & consultations.py"]
            AggR["dashboard.py & timeline.py"]
            SocR["community.py & notifications.py & privacy.py"]
        end
        
        subgraph BusinessServices ["Domain Services Layer"]
            DocSvc["document_service.py"]
            OcrSvc["ocr_service.py"]
            ExtrSvc["extraction_service.py"]
            BioSvc["biomarker_service.py"]
            CycleSvc["cycle_service.py"]
            NutriSvc["nutrition_service.py"]
            AssistSvc["assistant_service.py"]
            RetrSvc["retrieval_service.py"]
            RemSvc["reminder_service.py"]
            ConsSvc["consultation_service.py"]
            TimeSvc["timeline_service.py"]
            DashSvc["dashboard_service.py"]
            PrivSvc["privacy_service.py"]
        end

        subgraph CoreAndUtils ["Core & Safety Utils"]
            Guard["guardrails.py<br/>(Deterministic Red-Flags)"]
            Sec["security.py<br/>(Argon2 / JWT Rotation)"]
            Cfg["config.py<br/>(Pydantic Settings)"]
        end

        subgraph Repositories ["Repository Data Access Layer"]
            UserRepo["user_repo.py"]
            DocRepo["document_repo.py"]
            CycleRepo["cycle_repo.py"]
            NutriRepo["nutrition_repo.py"]
            RemRepo["reminder_repo.py"]
            ConsRepo["consultation_repo.py"]
            CommRepo["community_repo.py"]
        end

        subgraph Integrations ["External / Device Integrations"]
            LLM["llm_provider.py<br/>(Gemini 1.5 Flash / MockLLM)"]
            Storage["storage_provider.py<br/>(Private File System)"]
            Tess["pytesseract / PyMuPDF<br/>(Local OCR)"]
        end
    end

    subgraph DatabaseLayer ["Relational Storage"]
        DB[(SQLite / PostgreSQL<br/>SQLAlchemy 2.0 ORM)]
    end

    Client -->|HTTP / JSON| MW
    MW --> Router
    Router --> APISubmodules
    APISubmodules --> BusinessServices
    BusinessServices --> CoreAndUtils
    BusinessServices --> Integrations
    BusinessServices --> Repositories
    Repositories --> DB
```

---

## 3. Core Pipelines

### 3.1 Medical Document Ingestion & Extraction Pipeline
```mermaid
sequenceDiagram
    autonumber
    actor Patient
    participant API as reports.py
    participant Storage as storage_provider.py
    participant DocSvc as document_service.py
    participant OCR as ocr_service.py
    participant Extr as extraction_service.py
    participant DB as SQLite / PostgreSQL

    Patient->>API: POST /api/v1/reports/upload (PDF/Image)
    API->>Storage: Verify Magic Bytes (%PDF, PNG, JPG)
    Storage-->>API: Validated File Type & Private Path
    API->>DocSvc: process_uploaded_document()
    DocSvc->>DB: Insert MedicalDocument (status: processing)
    DocSvc->>OCR: extract_text_from_document()
    OCR->>OCR: PyMuPDF page text extraction (+ Tesseract fallback)
    OCR-->>DocSvc: Raw Text & Page Chunks
    DocSvc->>Extr: extract_biomarkers(pages_data)
    Extr->>Extr: Regex analyte matches (TSH, Insulin, LH, FSH, etc.)
    Extr->>Extr: Extract Lab Reference Ranges & Dates
    Extr-->>DocSvc: Extracted Biomarker Entities + Confidence
    DocSvc->>DB: Insert Biomarkers & Update Document (completed / needs_review)
    DocSvc-->>API: Document & Structured Lab Observations
    API-->>Patient: 201 Created (JSON Results)
```

### 3.2 Bilingual Assistant & Emergency Guardrail Flow
```mermaid
sequenceDiagram
    autonumber
    actor Patient
    participant API as assistant.py
    participant AssistSvc as assistant_service.py
    participant Guard as guardrails.py
    participant Retr as retrieval_service.py
    participant LLM as llm_provider.py
    participant DB as Database

    Patient->>API: POST /api/v1/assistant/chat (message, language)
    API->>AssistSvc: chat()
    AssistSvc->>Guard: check_urgent_symptoms(message, language)
    alt Emergency Red-Flag Detected (Acute Pain / Hemorrhage / Syncope)
        Guard-->>AssistSvc: is_urgent=True, Emergency Referral Notice
        AssistSvc-->>API: Immediate Urgent Care Response (Zero AI Latency)
        API-->>Patient: 🚨 Emergency Notice (Seek 112 / Emergency Dept)
    else Standard Query
        AssistSvc->>DB: Log User ChatMessage
        AssistSvc->>Retr: retrieve_relevant_passages(message)
        Retr-->>AssistSvc: Grounded Clinical Guidelines (Monash, ICMR-NIN)
        AssistSvc->>LLM: generate_response(prompt, context, language)
        LLM-->>AssistSvc: Answer Text + Citations
        AssistSvc->>Guard: sanitize_ai_output(answer)
        AssistSvc->>DB: Log Assistant ChatMessage
        AssistSvc-->>API: Structured Response (Answer, Sources, Safety Notice)
        API-->>Patient: 200 OK (Educational Guidance)
    end
```

---

## 4. Key Security Controls

1. **Authentication & Authorization**:
   - Short-lived Access JWTs (30m) and Rotating Refresh JWTs (7d).
   - Resource ownership enforcement: all repositories query by `user_id = current_user.id`.
2. **Private File Isolation**:
   - Uploaded files are stored in `private_uploads/user_{id}/{uuid}.{ext}`.
   - Files are never accessible via public HTTP static mounts.
   - Binary signature (magic bytes) validation prevents extension spoofing.
3. **Medical Privacy & Right to Erasure**:
   - `/api/v1/privacy/export`: Complete JSON export of all patient data.
   - `/api/v1/privacy/purge`: Requires `DELETE MY HEALTH DATA` verification phrase and cascades removal across all 13 database tables and physically wipes disk storage.
