import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

@pytest.fixture(scope='module')
def test_engine():
    """Provides an SQLAlchemy engine for tests."""
    return create_engine('sqlite:///:memory:')

@pytest.fixture(scope='module')
def tables(test_engine):
    """Creates all tables for testing."""
    Base.metadata.create_all(test_engine)
    yield
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
