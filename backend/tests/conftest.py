# tests/conftest.py
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.database import Base  # import your Base

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

# 3) Create tables in the in-memory DB once, before tests run:
Base.metadata.create_all(bind=engine)

@pytest.fixture
def db_session():
    """Yields a fresh SessionLocalTest() per test, then closes it."""
    session = SessionLocalTest()
    try:
        yield session
    finally:
        session.close()
