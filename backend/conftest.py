import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

@pytest.fixture(scope='session')
def test_engine():
    """Provides an SQLAlchemy engine for tests."""
    # Use SQLite in memory
    return create_engine('sqlite:///:memory:', echo=True)

@pytest.fixture(scope='session')
def tables(test_engine):
    """Creates all tables for testing in SQLite."""
    Base.metadata.create_all(test_engine)
    yield  # This is crucial to ensure that tables are created before tests are run
    Base.metadata.drop_all(test_engine)

@pytest.fixture
def db_session(test_engine, tables):
    """Yields a session and rolls back changes after each test."""
    connection = test_engine.connect()
    transaction = connection.begin()
    session = sessionmaker(bind=connection)()
    yield session
    session.close()
    transaction.rollback()
    connection.close()
