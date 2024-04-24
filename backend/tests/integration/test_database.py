import pytest
from sqlalchemy.exc import ProgrammingError
from models import *
from database import *  


def test_create_table_tutors_if_not_exists(db_session):
    # Ensure the table does not exist initially
    assert not db_session.bind.dialect.has_table(db_session.bind, 'tutors')

    # Call the function to create the table
    response = create_table_tutors_if_not_exists()

    # Verify the response message
    assert "created successfully" in response or "already exists" in response

    # Ensure the table exists after calling the function
    assert db_session.bind.dialect.has_table(db_session.bind, 'tutors')

    # Ensure the necessary foreign key relationships are established
    assert 'user_id' in Tutor.__table__.columns
    assert 'area_id' in Tutor.__table__.columns
    assert 'id' in User.__table__.columns
    assert 'id' in Area.__table__.columns

    # Check the constraint on slots column
    try:
        db_session.add(Tutor(slots=5))  # Attempt to insert a tutor without user_id and area_id
        db_session.commit()
    except ProgrammingError:
        db_session.rollback()
        assert True  # Constraint violation occurred
    else:
        assert False  # Constraint violation should have occurred

    # Clean up: Drop the table after testing
    Tutor.__table__.drop(db_session.bind)