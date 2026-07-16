from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class Student(Base):
    __tablename__ = "students"
    
    id = Column(Integer, primary_key=True, index=True)
    student_code = Column(String(20), unique=True, index=True, nullable=False)
    full_name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    status = Column(String(20), default="ACTIVE")

    registrations = relationship("Registration", back_populates="student")

class Workshop(Base):
    __tablename__ = "workshops"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    maximum_participants = Column(Integer, nullable=False)
    start_time = Column(DateTime, nullable=False)
    status = Column(String(20), default="OPEN")

    registrations = relationship("Registration", back_populates="workshop")

class Registration(Base):
    __tablename__ = "registrations"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    workshop_id = Column(Integer, ForeignKey("workshops.id"), nullable=False)
    registered_at = Column(DateTime, default=datetime.now)
    status = Column(String(20), default="REGISTERED") 

    student = relationship("Student", back_populates="registrations")
    workshop = relationship("Workshop", back_populates="registrations")