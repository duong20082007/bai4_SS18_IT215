from fastapi import FastAPI, Depends, status
from sqlalchemy.orm import Session
from typing import List

from database import engine, get_db, Base
from schemas import workshops as schemas
from services import workshops as services

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.post("/students", response_model=schemas.StudentResponse, status_code=status.HTTP_201_CREATED)
def create_student(payload: schemas.StudentCreate, db: Session = Depends(get_db)):
    return services.create_student(db, payload)

@app.get("/students", response_model=List[schemas.StudentResponse])
def get_students(db: Session = Depends(get_db)):
    return services.get_students(db)

@app.post("/workshops", response_model=schemas.WorkshopResponse, status_code=status.HTTP_201_CREATED)
def create_workshop(payload: schemas.WorkshopCreate, db: Session = Depends(get_db)):
    return services.create_workshop(db, payload)

@app.get("/workshops", response_model=List[schemas.WorkshopResponse])
def get_workshops(db: Session = Depends(get_db)):
    return services.get_workshops(db)

@app.get("/workshops/{workshop_id}", response_model=schemas.WorkshopResponse)
def get_workshop_detail(workshop_id: int, db: Session = Depends(get_db)):
    return services.get_workshop_detail(db, workshop_id)

@app.post("/registrations", response_model=schemas.RegistrationResponse, status_code=status.HTTP_201_CREATED)
def create_registration(payload: schemas.RegistrationCreate, db: Session = Depends(get_db)):
    return services.create_registration(db, payload)

@app.put("/registrations/{reg_id}/cancel", response_model=schemas.RegistrationResponse)
def cancel_registration(reg_id: int, db: Session = Depends(get_db)):
    return services.cancel_registration(db, reg_id)

@app.get("/students/{student_id}/workshops", response_model=schemas.StudentWorkshopsResponse)
def get_student_workshops(student_id: int, db: Session = Depends(get_db)):
    return services.get_student_workshops(db, student_id)

@app.get("/workshops/{workshop_id}/students", response_model=schemas.WorkshopStudentsResponse)
def get_workshop_students(workshop_id: int, db: Session = Depends(get_db)):
    return services.get_workshop_students(db, workshop_id)