import os
from typing import List, Union, Optional
from urllib.parse import urlparse, quote_plus
from pydantic import field_validator, model_validator, ConfigDict
from pydantic_settings import BaseSettings


def normalize_postgres_url(url: Optional[str]) -> Optional[str]:
    """Ensures PostgreSQL URLs use the postgresql+psycopg:// driver syntax for SQLAlchemy 2."""
    if not url:
        return url
    trimmed = url.strip()
    if trimmed.startswith("postgresql://"):
        return "postgresql+psycopg://" + trimmed[len("postgresql://"):]
    elif trimmed.startswith("postgres://"):
        return "postgresql+psycopg://" + trimmed[len("postgres://"):]
    return trimmed


class Settings(BaseSettings):
    PROJECT_NAME: str = "Health Saathi"
    VERSION: str = "1.0.0"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    PORT: int = 8000

    # Security & Authentication
    SECRET_KEY: str = "development_secret_key_change_in_production_min_32_chars"
    JWT_SECRET_KEY: Optional[str] = None
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # Database Configuration
    DATABASE_URL: str = "sqlite:///./health_saathi.db"
    DIRECT_URL: Optional[str] = None
    
    # Connection Pool Settings (Optimized for Supabase Transaction Pooler)
    DATABASE_POOL_SIZE: int = 10
    DATABASE_MAX_OVERFLOW: int = 20
    DATABASE_POOL_TIMEOUT: int = 30
    DATABASE_POOL_RECYCLE: int = 1800

    # Uploads & Storage
    UPLOAD_DIR: str = "./uploads/private"
    MAX_UPLOAD_SIZE_MB: int = 10
    MAX_UPLOAD_SIZE_BYTES: int = 10 * 1024 * 1024

    # LLM & AI Services
    LLM_PROVIDER: str = "mock"  # "mock", "gemini", "openai"
    LLM_MODEL: str = "gemini-1.5-flash"
    GEMINI_API_KEY: str = ""
    OPENAI_API_KEY: str = ""

    # OCR
    TESSERACT_CMD: str = ""

    # CORS
    CORS_ORIGINS: Union[List[str], str] = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000"
    ]
    BACKEND_CORS_ORIGINS: Union[List[str], str] = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000"
    ]

    # Demo Mode
    DEMO_MODE: bool = True
    ENABLE_DEMO_SEED: bool = True
    DEMO_USER_EMAIL: str = "priya@healthsaathi.in"
    DEMO_USER_PASSWORD: str = "DemoUserPassword123!"

    @field_validator("CORS_ORIGINS", "BACKEND_CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> List[str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",") if i.strip()]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    @field_validator("DATABASE_URL", mode="before")
    @classmethod
    def assemble_database_url(cls, v: str) -> str:
        if not v:
            return "sqlite:///./health_saathi.db"
        return normalize_postgres_url(v) or v

    @field_validator("DIRECT_URL", mode="before")
    @classmethod
    def assemble_direct_url(cls, v: Optional[str]) -> Optional[str]:
        if not v:
            return None
        return normalize_postgres_url(v)

    @model_validator(mode="after")
    def post_process_settings(self):
        # Synchronize JWT_SECRET_KEY and SECRET_KEY
        if self.JWT_SECRET_KEY:
            self.SECRET_KEY = self.JWT_SECRET_KEY
        elif self.SECRET_KEY:
            self.JWT_SECRET_KEY = self.SECRET_KEY

        # Production safety enforcement
        if self.ENVIRONMENT == "production":
            self.DEMO_MODE = False
            self.ENABLE_DEMO_SEED = False
            if "development_secret_key" in self.SECRET_KEY or len(self.SECRET_KEY) < 32:
                raise ValueError(
                    "Production safety violation: SECRET_KEY must be set to a secure, random string (min 32 chars) in production."
                )
            if self.DATABASE_URL.startswith("sqlite"):
                raise ValueError(
                    "Production safety violation: Production requires a Supabase PostgreSQL connection string in DATABASE_URL. SQLite is not permitted."
                )
        return self

    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )


settings = Settings()

os.makedirs(settings.UPLOAD_DIR, exist_ok=True)

