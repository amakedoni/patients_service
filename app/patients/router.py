from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from typing import List

from app.db.session import get_db
from app.patients import service
from app.patients.schemas.user import UserCreate, UserOut
from app.patients.schemas.schedule import ScheduleCreate, ScheduleOut
from app.patients.schemas.medicine import MedicineCreate, MedicineOut
from app.patients.schemas.intake import IntakeCreate, IntakeOut

router = APIRouter()

@router.post("/users", response_model=UserOut)
async def create_user(user_in: UserCreate, db: AsyncSession = Depends(get_db)):
    user = await service.create_user(db, user_in)
    return user

@router.get("/users/{user_id}", response_model=UserOut)
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    u = await service.get_user(db, user_id)
    if not u:
        raise HTTPException(status_code=404, detail="user not found")
    return u

@router.get("/users", response_model=List[UserOut])
async def list_users(db: AsyncSession = Depends(get_db)):
    return await service.list_users(db)

@router.post("/schedules", response_model=ScheduleOut)
async def create_schedule(schedule_in: ScheduleCreate, db: AsyncSession = Depends(get_db)):
    return await service.create_schedule(db, schedule_in)

@router.post("/medicines", response_model=MedicineOut)
async def create_medicine(med_in: MedicineCreate, db: AsyncSession = Depends(get_db)):
    # minimal validation: ensure patient and schedule exist
    from app.patients.models.user import User
    from app.patients.models.schedule import Schedule
    user = await db.get(User, med_in.patient_id)
    if not user:
        raise HTTPException(status_code=404, detail="patient not found")
    
    schedule = await db.get(Schedule, med_in.schedules_id)
    if not schedule:
        raise HTTPException(status_code=404, detail="schedule not found")
    
    return await service.create_medicine(db, med_in)

@router.get("/patients/{patient_id}/medicines", response_model=List[MedicineOut])
async def list_meds(patient_id: int, db: AsyncSession = Depends(get_db)):
    return await service.list_medicines_for_patient(db, patient_id)

@router.post("/intake", response_model=IntakeOut)
async def create_intake(intake_in: IntakeCreate, db: AsyncSession = Depends(get_db)):
    return await service.create_intake(db, intake_in)

@router.get("/patients/{patient_id}/intake", response_model=List[IntakeOut])
async def list_intake(patient_id: int, db: AsyncSession = Depends(get_db)):
    return await service.list_intake_for_patient(db, patient_id)

@router.get("/ping")
async def ping():
    from app.db.session import engine
    async with engine.connect() as conn:
        result = await conn.execute(text("SELECT 1"))
        return {"db": bool(result.scalar())}
