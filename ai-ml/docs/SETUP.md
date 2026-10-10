# ⚙️ Step-by-Step Setup Guide

This guide enables quick local deployment for hackathon judging and development.

---

## Prerequisites
- **Python**: Version 3.10 or higher
- **Node.js**: Version 18.x or higher (`node -v`, `npm -v`)
- **Git**

---

## 1. Backend Setup

```bash
# 1. Open a terminal and enter the backend directory
cd backend

# 2. Create a virtual environment
python -m venv venv

# 3. Activate the virtual environment
# Windows (PowerShell):
venv\Scripts\Activate.ps1
# Windows (CMD):
venv\Scripts\activate.bat
# macOS / Linux:
source venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Populate synthetic demonstration data
python ../database/seed_data.py

# 6. Start the FastAPI development server
uvicorn app.main:app --reload --port 8000
```

Verify backend operation:
- Health check: `http://localhost:8000/health`
- Interactive Swagger UI: `http://localhost:8000/docs`

---

## 2. Frontend Setup

```bash
# 1. Open a second terminal and navigate to the frontend directory
cd frontend

# 2. Install Node dependencies
npm install

# 3. Start the Vite development server
npm run dev
```

Open your browser at `http://localhost:5173`.

---

## 3. Running Backend Tests

```bash
# In the backend terminal (with venv activated)
pytest ../tests -v
```
All unit tests and safety guardrail checks should pass.
