from pydantic import BaseModel
from typing import Optional
from enum import Enum

class MedicineForm(str, Enum):
    tablet = "tablet"
    drop = "drop"
    spray = "spray"
    solution = "solution"
    injection = "injection"
    powder = "powder"
    inhaler = "inhaler"
    other = "other"

class MedicineUnit(str, Enum):
    mg = "mg"
    g = "g"
    pcs = "pcs"
    ml = "ml"
    caps = "caps."
    dose = "dose"

class MedicineCreate(BaseModel):
    patient_id: int
    schedules_id: int
    name: str
    form: MedicineForm
    unit: MedicineUnit
    dosage: float
    instructions: Optional[str] = None

class MedicineOut(MedicineCreate):
    id: int
    created_at: Optional[str]

    class Config:
        orm_mode = True
