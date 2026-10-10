import pytest
import os
from typing import Generator
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool

# Set test environment flags
os.environ["DATABASE_URL"] = "sqlite:///:memory:"
os.environ["SECRET_KEY"] = "test-secret-key-for-health-saathi-testing-only"
os.environ["ENVIRONMENT"] = "testing"
os.environ["LLM_PROVIDER"] = "mock"

from app.db.base import Base
from app.db.session import get_db
from app.main import app
from app.core.security import create_access_token, get_password_hash
from app.models.user import User
from app.models.profile import HealthProfile

# Create in-memory SQLite database for testing
TEST_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def db() -> Generator[Session, None, None]:
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    
    yield session
    
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture
def client(db: Session) -> Generator[TestClient, None, None]:
    def override_get_db():
        try:
            yield db
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def test_user(db: Session) -> User:
    user = User(
        email="test_user@healthsaathi.in",
        hashed_password=get_password_hash("StrongTestPass123!"),
        full_name="Test Patient",
        is_active=True,
        is_verified=True,
        consent_given=True
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    profile = HealthProfile(
        user_id=user.id,
        age=25,
        diet_type="veg",
        baseline_cycle_length=32,
        period_duration=4,
        preferred_language="en",
        timezone="Asia/Kolkata"
    )
    db.add(profile)
    db.commit()
    return user


@pytest.fixture
def auth_headers(test_user: User) -> dict:
    token = create_access_token({"sub": test_user.email, "user_id": test_user.id})
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def other_user(db: Session) -> User:
    user = User(
        email="other_user@healthsaathi.in",
        hashed_password=get_password_hash("StrongTestPass123!"),
        full_name="Other Patient",
        is_active=True,
        is_verified=True,
        consent_given=True
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@pytest.fixture
def other_auth_headers(other_user: User) -> dict:
    token = create_access_token({"sub": other_user.email, "user_id": other_user.id})
    return {"Authorization": f"Bearer {token}"}
