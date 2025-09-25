from pydantic import BaseModel
from typing import List, Optional
import datetime

class IntakeBase(BaseModel):
    taken_at: Optional[datetime.datetime] = None
    taken: bool

class IntakeCreate(IntakeBase):
    prescription_id: int

class Intake(IntakeBase):
    id: int
    class Config:
        orm_mode = True

class PrescriptionBase(BaseModel):
    drug_name: str
    dosage: str

class PrescriptionCreate(PrescriptionBase):
    patient_id: int

class Prescription(PrescriptionBase):
    id: int
    intakes: List[Intake] = []
    class Config:
        orm_mode = True

class PatientBase(BaseModel):
    name: str
    birth_date: Optional[str] = None

class PatientCreate(PatientBase):
    pass

class Patient(PatientBase):
    id: int
    prescriptions: List[Prescription] = []
    class Config:
        orm_mode = True
