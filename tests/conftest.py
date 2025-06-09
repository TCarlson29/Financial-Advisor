import sys, os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.insert(0, PROJECT_ROOT)

from backend.main import app, get_db
import backend.models
from backend.database import Base

_TEST_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    _TEST_DATABASE_URL, connect_args={"check_same_thread": False},
    poolclass=StaticPool,# << ensures the same memory DB is used
)

TestingSessionLocal  = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)

# 1) This runs before *each* test function and resets the schema
@pytest.fixture(autouse=True)
def reset_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

# 2) A session scoped to each test
@pytest.fixture
def db_session():
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()

# 3) A TestClient that uses our in-memory session
@pytest.fixture
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()
