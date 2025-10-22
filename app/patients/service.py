from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from sqlalchemy import select

from app.patients.models.user import User
from app.patients.models.medicine import Medicine
from app.patients.models.schedule import Schedule
from app.patients.models.intake import IntakeHistory

from app.patients.schemas.user import UserCreate
from app.patients.schemas.medicine import MedicineCreate
from app.patients.schemas.schedule import ScheduleCreate
from app.patients.schemas.intake import IntakeCreate

async def create_user(db: AsyncSession, user_in: UserCreate) -> User:
    user = User(hash_password=user_in.hash_password)
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user

async def get_user(db: AsyncSession, user_id: int) -> Optional[User]:
    return await db.get(User, user_id)

async def list_users(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[User]:
    result = await db.execute(select(User).offset(skip).limit(limit))
    return result.scalars().all()

async def create_schedule(db: AsyncSession, obj_in: ScheduleCreate) -> Schedule:
    obj = Schedule(**obj_in.dict())
    db.add(obj)
    await db.commit()
    await db.refresh(obj)
    return obj

async def create_medicine(db: AsyncSession, obj_in: MedicineCreate) -> Medicine:
    obj = Medicine(**obj_in.dict())
    db.add(obj)
    await db.commit()
    await db.refresh(obj)
    return obj

async def list_medicines_for_patient(db: AsyncSession, patient_id: int) -> List[Medicine]:
    result = await db.execute(
        select(Medicine).filter(Medicine.patient_id == patient_id)
    )
    return result.scalars().all()

async def create_intake(db: AsyncSession, obj_in: IntakeCreate) -> IntakeHistory:
    obj = IntakeHistory(**obj_in.dict())
    db.add(obj)
    await db.commit()
    await db.refresh(obj)
    return obj

async def list_intake_for_patient(db: AsyncSession, patient_id: int) -> List[IntakeHistory]:
    result = await db.execute(
        select(IntakeHistory)
        .filter(IntakeHistory.patient_id == patient_id)
        .order_by(IntakeHistory.created_at.desc())
    )
    return result.scalars().all()
