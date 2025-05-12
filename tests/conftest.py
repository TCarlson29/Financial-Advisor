import sys, os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.insert(0, PROJECT_ROOT)

from backend.main import app

@pytest.fixture
def client():
    return TestClient(app)
from backend.database import Base  # import your Base
import backend.models

# 1) Create an in-memory SQLite engine:
_TEST_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    _TEST_DATABASE_URL, connect_args={"check_same_thread": False}
)

# 2) Create a sessionmaker bound to that engine:
SessionLocalTest = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)

Base.metadata.create_all(bind=engine)

@pytest.fixture
def db_session():
    """Yields a fresh SessionLocalTest() per test, then closes it."""
    session = SessionLocalTest()
    try:
        yield session
    finally:
        session.close()
