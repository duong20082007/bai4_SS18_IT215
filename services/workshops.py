from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from datetime import datetime
from models.workshops import Student, Workshop, Registration
from schemas import workshops as schemas

def create_student(db: Session, payload: schemas.StudentCreate):
    if db.query(Student).filter(Student.student_code == payload.student_code).first():
        raise HTTPException(status_code=400, detail="Student code already exists")
    if db.query(Student).filter(Student.email == payload.email).first():
        raise HTTPException(status_code=400, detail="Email already exists")
    
    new_student = Student(**payload.model_dump())
    db.add(new_student)
    db.commit()
    db.refresh(new_student)
    return new_student

def get_students(db: Session):
    return db.query(Student).all()

def create_workshop(db: Session, payload: schemas.WorkshopCreate):
    new_workshop = Workshop(**payload.model_dump())
    db.add(new_workshop)
    db.commit()
    db.refresh(new_workshop)
    return new_workshop

def get_workshops(db: Session):
    return db.query(Workshop).all()

def get_workshop_detail(db: Session, workshop_id: int):
    workshop = db.query(Workshop).filter(Workshop.id == workshop_id).first()
    if not workshop:
        raise HTTPException(status_code=404, detail="Workshop not found")
    return workshop

def create_registration(db: Session, payload: schemas.RegistrationCreate):
    student = db.query(Student).filter(Student.id == payload.student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    if student.status != "ACTIVE":
        raise HTTPException(status_code=400, detail="Student is not active")

    workshop = db.query(Workshop).filter(Workshop.id == payload.workshop_id).first()
    if not workshop:
        raise HTTPException(status_code=404, detail="Workshop not found")
    if workshop.status != "OPEN":
        raise HTTPException(status_code=400, detail="Workshop is not open for registration")
    if workshop.start_time < datetime.now():
        raise HTTPException(status_code=400, detail="Workshop has already started")

    existing_reg = db.query(Registration).filter(
        Registration.student_id == payload.student_id,
        Registration.workshop_id == payload.workshop_id,
        Registration.status == "REGISTERED"
    ).first()
    if existing_reg:
        raise HTTPException(status_code=400, detail="Student already registered for this workshop")

    current_count = db.query(Registration).filter(
        Registration.workshop_id == payload.workshop_id,
        Registration.status == "REGISTERED"
    ).count()
    if current_count >= workshop.maximum_participants:
        raise HTTPException(status_code=400, detail="Workshop has reached maximum capacity")

    new_reg = Registration(student_id=payload.student_id, workshop_id=payload.workshop_id)
    db.add(new_reg)
    db.commit()
    db.refresh(new_reg)
    return new_reg

def cancel_registration(db: Session, reg_id: int):
    reg = db.query(Registration).filter(Registration.id == reg_id).first()
    if not reg:
        raise HTTPException(status_code=404, detail="Registration not found")
    if reg.status == "CANCELLED":
        raise HTTPException(status_code=400, detail="Registration is already cancelled")
    
    reg.status = "CANCELLED"
    db.commit()
    db.refresh(reg)
    return reg

def get_student_workshops(db: Session, student_id: int):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    workshops = (
        db.query(Workshop).join(Registration).filter(Registration.student_id == student_id, Registration.status == "REGISTERED").all()
    )
    return {"student": student, "workshops": workshops}

def get_workshop_students(db: Session, workshop_id: int):
    workshop = db.query(Workshop).filter(Workshop.id == workshop_id).first()
    if not workshop:
        raise HTTPException(status_code=404, detail="Workshop not found")
    
    students = (
        db.query(Student).join(Registration).filter(Registration.workshop_id == workshop_id, Registration.status == "REGISTERED").all()
    )
    return {"workshop": workshop, "students": students}