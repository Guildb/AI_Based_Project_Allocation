from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm import declarative_base
Base = declarative_base()



class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    firstName = Column(String, nullable=False)
    lastName = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    type = Column(String, nullable=False)
    
    students = relationship("Student", back_populates="user")
    tutors = relationship("Tutor", back_populates="user")
    
class Student(Base):
    __tablename__ = 'students'
    id = Column(Integer, primary_key=True)
    student_number = Column(String, nullable=False)
    area_id = Column(Integer, ForeignKey('areas.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    
    area = relationship("Area")
    user = relationship("User", back_populates="students")

class Tutor(Base):
    __tablename__ = 'tutors'
    id = Column(Integer, primary_key=True)
    slots = Column(Integer, nullable=False)
    area_id = Column(Integer, ForeignKey('areas.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    
    area = relationship("Area")
    user = relationship("User", back_populates="tutors")

class Area(Base):
    __tablename__ = 'areas'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    
class Expertise(Base):
    __tablename__ = 'expertises'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    acronym = Column(String, nullable=False)
    area_id = Column(Integer, ForeignKey('areas.id'))
    
    area = relationship("Area")

class Project(Base):
    __tablename__ = 'projects'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    student_id = Column(Integer, ForeignKey('students.id'))
    tutor_id = Column(Integer, ForeignKey('tutors.id'))
    area_id = Column(Integer, ForeignKey('areas.id'))
    alocated = Column(Boolean, default=False)

    student = relationship("Student")
    tutor = relationship("Tutor")
    area = relationship("Area")
    
class Tutor_expertise(Base):
    __tablename__ = 'tutor_expertise'
    id = Column(Integer, primary_key=True)
    tutor_id = Column(Integer, ForeignKey('tutors.id'))
    expertise_id = Column(Integer, ForeignKey('expertises.id'))

    tutor = relationship("Tutor")
    expertise = relationship("Expertise")

class Project_expertise(Base):
    __tablename__ = 'project_expertise'
    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey('projects.id'))
    expertise_id = Column(Integer, ForeignKey('expertises.id'))

    project = relationship("Project")
    expertise = relationship("Expertise")

