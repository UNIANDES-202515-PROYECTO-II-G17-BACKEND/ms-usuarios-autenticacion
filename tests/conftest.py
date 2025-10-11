import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.app import app
from src.dependencies import get_session
from src.domain.models import Base
import os

# --- Database Setup for Tests ---
TEST_DB_PATH = "./test_db.sqlite"
SQLALCHEMY_DATABASE_URL = f"sqlite:///{TEST_DB_PATH}"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# --- Override get_session to provide a session without transaction management ---
def override_get_session():
    """
    This dependency override provides a test database session.
    Transaction management is now handled by the application code.
    """
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_session] = override_get_session


# --- Main Test Client Fixture ---
@pytest.fixture(scope="function")
def client():
    Base.metadata.create_all(bind=engine)
    with TestClient(app) as c:
        yield c
    Base.metadata.drop_all(bind=engine)


# --- Final Cleanup Fixture ---
@pytest.fixture(scope="session", autouse=True)
def final_cleanup(request):
    """
    A session-scoped fixture to ensure the database file is properly cleaned up.
    """
    yield
    TestingSessionLocal.close_all()
    engine.dispose()
    if os.path.exists(TEST_DB_PATH):
        os.remove(TEST_DB_PATH)
