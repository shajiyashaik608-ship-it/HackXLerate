from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.logging import logger
from app.core.exceptions import setup_exception_handlers
from app.middleware.security import SecurityHeadersMiddleware
from app.db.session import engine
from app.db.base import Base
import app.models  # Register all SQLAlchemy models with metadata
from app.api.router import api_router
from app.services.ocr_service import ocr_service
from app.services.nutrition_service import nutrition_service
from app.db.session import SessionLocal


from sqlalchemy import text

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: ensure tables exist in dev SQLite; in PostgreSQL/production migrations are managed via Alembic
    if settings.DATABASE_URL.startswith("sqlite") and settings.ENVIRONMENT != "production":
        logger.info("Initializing Health Saathi local development SQLite schema...")
        Base.metadata.create_all(bind=engine)
    else:
        logger.info("Connecting to PostgreSQL database (Supabase). Schema managed via Alembic migrations.")
    
    # Seed default nutritional data if database is accessible and empty
    db = SessionLocal()
    try:
        nutrition_service.ensure_default_meals_seeded(db)
    except Exception as e:
        logger.warning(f"Default nutritional meals initialization skipped: {e}")
    finally:
        db.close()
    yield
    # Shutdown
    logger.info("Health Saathi backend shutting down.")


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="AI-Powered Personal Health Copilot for PCOS awareness, menstrual tracking, Indian nutrition, and medical report understanding.",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Exception handlers
setup_exception_handlers(app)

# Security and Request Tracing Middleware
app.add_middleware(SecurityHeadersMiddleware)

# CORS Configuration
origins = getattr(settings, "BACKEND_CORS_ORIGINS", None) or getattr(settings, "CORS_ORIGINS", None) or ["http://localhost:5173", "http://127.0.0.1:5173"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health & Readiness Checks
@app.get("/health", tags=["System"])
def health_check():
    return {
        "status": "online",
        "service": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "environment": settings.ENVIRONMENT,
        "guardrails_active": True,
        "message": "Health Saathi core service is operational."
    }


@app.get("/readiness", tags=["System"])
def readiness_check():
    # Verify DB connectivity securely without exposing credentials
    db_ok = False
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
            db_ok = True
    except Exception as e:
        logger.error(f"Readiness check database connection failed: {type(e).__name__}")
        db_ok = False

    return {
        "status": "ready" if db_ok else "degraded",
        "database_connected": db_ok,
        "database_backend": "postgresql" if ("postgres" in settings.DATABASE_URL or "psycopg" in settings.DATABASE_URL) else "sqlite",
        "ocr_available": ocr_service.is_ocr_installed(),
        "llm_provider": settings.LLM_PROVIDER,
        "demo_mode": getattr(settings, "DEMO_MODE", False)
    }



# Mount API Router
app.include_router(api_router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=settings.PORT, reload=True)
