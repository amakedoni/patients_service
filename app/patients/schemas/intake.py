from pydantic import BaseModel
from typing import Optional
from datetime import time, datetime

class IntakeCreate(BaseModel):
    medicine_id: int
    patient_id: int
    planned_time: Optional[time] = None
    datetime: Optional[datetime] = None
    taken: Optional[bool] = False
    skipped: Optional[bool] = False
    dose_taken: Optional[float] = None
    synced: Optional[bool] = False

class IntakeOut(IntakeCreate):
    id: int
    created_at: Optional[str]

    class Config:
        orm_mode = True
