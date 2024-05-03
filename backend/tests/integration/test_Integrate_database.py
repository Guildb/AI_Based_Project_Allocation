import pytest
from sqlalchemy.exc import ProgrammingError
from sqlalchemy.exc import IntegrityError
from models import *
from database import *  

##Testing tables relationships
def test_user_student_relationship(db_session):
    user = User(firstName="Alice", lastName="Johnson", email="alice.johnson@example.com", password="password", type="student")
    db_session.add(user)
    db_session.commit()

    student = Student(student_number="S123456", user_id=user.id)
    db_session.add(student)
    db_session.commit()

    retrieved_student = db_session.query(Student).filter_by(student_number="S123456").first()
    assert retrieved_student is not None
    assert retrieved_student.user.email == "alice.johnson@example.com"

def test_user_tutor_relationship(db_session):
    user = User(firstName="Alice", lastName="Johnson", email="alice.johnson@example.com", password="password", type="tutor")
    db_session.add(user)
    db_session.commit()
    
    area = Area(name="it")
    db_session.add(area)
    db_session.commit()

    tutor = Tutor(slots="5", area_id=area.id, user_id =user.id )
    db_session.add(tutor)
    db_session.commit()

    retrieved_tutor = db_session.query(Tutor).filter_by(user_id=user.id).first()
    assert retrieved_tutor is not None
    assert retrieved_tutor.user.email == "alice.johnson@example.com"
    
def test_area_expertise_relationship(db_session):    
    area = Area(name="it")
    db_session.add(area)
    db_session.commit()

    expertise = Expertise(name="Artificial Inteligence", acronym="AI", area_id =area.id )
    db_session.add(expertise)
    db_session.commit()

    retrieved_expertise = db_session.query(Expertise).filter_by(id=expertise.id).first()
    assert retrieved_expertise is not None
    assert retrieved_expertise.name == "Artificial Inteligence"
    assert retrieved_expertise.area_id == area.id
    
def test_tutor_expertise_relationship(db_session):
    user = User(firstName="Alice", lastName="Johnson", email="alice.johnson@example.com", password="password", type="tutor")
    db_session.add(user)
    db_session.commit()
    
    area = Area(name="it")
    db_session.add(area)
    db_session.commit()

    tutor = Tutor(slots="5", area_id=area.id, user_id =user.id )
    db_session.add(tutor)
    db_session.commit()
    
    expertise = Expertise(name="Artificial Inteligence", acronym="AI", area_id =area.id )
    db_session.add(expertise)
    db_session.commit()
    
    tutor_expert = Tutor_expertise(tutor_id = tutor.id, expertise_id = expertise.id)
    db_session.add(tutor_expert)
    db_session.commit()

    retrieved_tutor_expertise = db_session.query(Tutor_expertise).filter_by(tutor_id=tutor.id).first()
    assert retrieved_tutor_expertise is not None
    assert retrieved_tutor_expertise.expertise_id == expertise.id   

def test_project_all_relationship(db_session):
    user = User(firstName="Alice", lastName="Johnson", email="alice.johnson@example.com", password="password", type="tutor")
    db_session.add(user)
    db_session.commit()
    
    area = Area(name="it")
    db_session.add(area)
    db_session.commit()

    tutor = Tutor(slots="5", area_id=area.id, user_id =user.id )
    db_session.add(tutor)
    db_session.commit()
    
    
    expertise = Expertise(name="Artificial Inteligence", acronym="AI", area_id =area.id )
    db_session.add(expertise)
    db_session.commit()
    
    
    project = Project(name="ai based project alocation", description="alocate project to tutors", student_id=None , tutor_id=tutor.id, area_id= area.id, alocated = False)
    db_session.add(project)
    db_session.commit()


    retrieved_project = db_session.query(Project).filter_by(name="ai based project alocation").first()
    assert retrieved_project is not None
    assert retrieved_project.tutor_id == tutor.id 

def test_project_expertise_relationship(db_session):
    user = User(firstName="Alice", lastName="Johnson", email="alice.johnson@example.com", password="password", type="tutor")
    db_session.add(user)
    db_session.commit()
    
    area = Area(name="it")
    db_session.add(area)
    db_session.commit()

    tutor = Tutor(slots="5", area_id=area.id, user_id =user.id )
    db_session.add(tutor)
    db_session.commit()
    
    
    expertise = Expertise(name="Artificial Inteligence", acronym="AI", area_id =area.id )
    db_session.add(expertise)
    db_session.commit()
    
    
    project = Project(name="ai based project alocation", description="alocate project to tutors", student_id=None , tutor_id=tutor.id, area_id= area.id, alocated = False)
    db_session.add(project)
    db_session.commit()
    
    project_expert = Project_expertise(project_id=project.id, expertise_id=expertise.id)
    db_session.add(project_expert)
    db_session.commit()


    retrieved_project_expertise = db_session.query(Project_expertise).filter_by(project_id=project.id).first()
    assert retrieved_project_expertise is not None
    assert retrieved_project_expertise.expertise_id == expertise.id 
    
    
##Testing adding 2 users with same email
def test_duplicate_user_email(db_session):
    user1 = User(firstName="Alice", lastName="Johnson", email="alice.johnson@example.com", password="password", type="student")
    db_session.add(user1)
    db_session.commit()

    try:
        user2 = User(firstName="Bob", lastName="Smith", email="alice.johnson@example.com", password="password", type="student")
        db_session.add(user2)
        db_session.commit()
    except Exception as e:
        print(f"Exception: {e}")
        assert "constraint" in str(e).lower()

##Testing Delete constrains
def test_delete_user_before_student(db_session):
    user = User(firstName="Alice", lastName="Johnson", email="alice.johnson@example.com", password="password", type="student")
    db_session.add(user)
    db_session.commit()

    student = Student(student_number="S123456", user_id=user.id)
    db_session.add(student)
    db_session.commit()

    try:
        db_session.delete(user)
        db_session.commit()
    except Exception as e:
        print(f"Exception: {e}")
        assert "constraint" in str(e).lower()
  
def test_delete_user_before_tutor(db_session):
    user = User(firstName="Alice", lastName="Johnson", email="alice.johnson@example.com", password="password", type="tutor")
    db_session.add(user)
    db_session.commit()
    
    area = Area(name="it")
    db_session.add(area)
    db_session.commit()

    tutor = Tutor(slots="5", area_id=area.id, user_id =user.id )
    db_session.add(tutor)
    db_session.commit()

    try:
        db_session.delete(user)
        db_session.commit()
    except Exception as e:
        print(f"Exception: {e}")
        assert "constraint" in str(e).lower()

def test_delete_area_before_expertise(db_session):
    area = Area(name="it")
    db_session.add(area)
    db_session.commit()

    expertise = Expertise(name="Artificial Inteligence", acronym="AI", area_id =area.id )
    db_session.add(expertise)
    db_session.commit()

    try:
        db_session.delete(area)
        db_session.commit()
    except Exception as e:
        print(f"Exception: {e}")
        assert False    
    
def test_delete_tutor_before_expertise(db_session):
    user = User(firstName="Alice", lastName="Johnson", email="alice.johnson@example.com", password="password", type="tutor")
    db_session.add(user)
    db_session.commit()
    
    area = Area(name="it")
    db_session.add(area)
    db_session.commit()

    tutor = Tutor(slots="5", area_id=area.id, user_id =user.id )
    db_session.add(tutor)
    db_session.commit()
    
    expertise = Expertise(name="Artificial Inteligence", acronym="AI", area_id =area.id )
    db_session.add(expertise)
    db_session.commit()
    
    tutor_expert = Tutor_expertise(tutor_id = tutor.id, expertise_id = expertise.id)
    db_session.add(tutor_expert)
    db_session.commit()

    try:
        db_session.delete(tutor)
        db_session.commit()
    except Exception as e:
        print(f"Exception: {e}")
        assert False
        
def test_delete_expertise_before_project(db_session):
    user = User(firstName="Alice", lastName="Johnson", email="alice.johnson@example.com", password="password", type="tutor")
    db_session.add(user)
    db_session.commit()
    
    area = Area(name="it")
    db_session.add(area)
    db_session.commit()

    tutor = Tutor(slots="5", area_id=area.id, user_id =user.id )
    db_session.add(tutor)
    db_session.commit()    
    
    expertise = Expertise(name="Artificial Inteligence", acronym="AI", area_id =area.id )
    db_session.add(expertise)
    db_session.commit()
    
    
    project = Project(name="ai based project alocation", description="alocate project to tutors", student_id=None , tutor_id=tutor.id, area_id= area.id, alocated = False)
    db_session.add(project)
    db_session.commit()
    
    project_expert = Project_expertise(project_id=project.id, expertise_id=expertise.id)
    db_session.add(project_expert)
    db_session.commit()

    try:
        db_session.delete(project)
        db_session.commit()
    except Exception as e:
        print(f"Exception: {e}")
        assert False      
    
  
    
    
    
    
    
    
    
    
    