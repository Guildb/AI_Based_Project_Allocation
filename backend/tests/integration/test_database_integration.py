import pytest
from models import Project, Student, Tutor, Area, Expertise, Tutor_expertise, Project_expertise
from database import *  


def test_create_table_projects(db_session):
    # Assuming your function modifies the database schema directly
    # First, we simulate the environment before the function call
    assert db_session.query(Project).count() == 0

    # Call your function which is supposed to create the table
    response = create_table_projects_if_not_exists()
    assert "created successfully" in response or "already exists" in response

    # Test creating a project entry
    student = Student()
    tutor = Tutor()
    area = Area()
    db_session.add_all([student, tutor, area])
    db_session.commit()

    project = Project(name="AI Research", description="Deep learning project", student_id=student.id, tutor_id=tutor.id, area_id=area.id, alocated=False)
    db_session.add(project)
    db_session.commit()

    # Verify that the project was added correctly
    assert db_session.query(Project).count() == 1
    assert db_session.query(Project).first().name == "AI Research"
