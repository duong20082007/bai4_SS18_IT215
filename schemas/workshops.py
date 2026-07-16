from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional

class StudentCreate(BaseModel):
    student_code: str
    full_name: str
    email: str
    status: Optional[str] = "ACTIVE"

class StudentResponse(StudentCreate):
    id: int
    class Config:
        from_attributes = True

class WorkshopCreate(BaseModel):
    title: str
    description: Optional[str] = None
    maximum_participants: int
    start_time: datetime
    status: Optional[str] = "OPEN"

class WorkshopResponse(WorkshopCreate):
    id: int
    class Config:
        from_attributes = True

class RegistrationCreate(BaseModel):
    student_id: int
    workshop_id: int

class RegistrationResponse(BaseModel):
    id: int
    student_id: int
    workshop_id: int
    registered_at: datetime
    status: str
    class Config:
        from_attributes = True

class StudentWorkshopsResponse(BaseModel):
    student: StudentResponse
    workshops: List[WorkshopResponse]

class WorkshopStudentsResponse(BaseModel):
    workshop: WorkshopResponse
    students: List[StudentResponse]