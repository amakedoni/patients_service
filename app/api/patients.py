from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.core.db import get_db
from app import models, schemas

router = APIRouter()

# ------------------- PATIENTS -------------------

@router.post("/", response_model=schemas.Patient)
async def create_patient(patient: schemas.PatientCreate, db: AsyncSession = Depends(get_db)):
    db_patient = models.Patient(**patient.dict())
    db.add(db_patient)
    await db.commit()
    await db.refresh(db_patient)
    return db_patient

@router.get("/{patient_id}", response_model=schemas.Patient)
async def get_patient(patient_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Patient).where(models.Patient.id == patient_id))
    patient = result.scalar_one_or_none()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient

@router.get("/", response_model=list[schemas.Patient])
async def list_patients(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Patient))
    return result.scalars().all()

@router.delete("/{patient_id}")
async def delete_patient(patient_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Patient).where(models.Patient.id == patient_id))
    patient = result.scalar_one_or_none()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    await db.delete(patient)
    await db.commit()
    return {"detail": f"Patient {patient_id} deleted"}

# ------------------- PRESCRIPTIONS -------------------

@router.post("/{patient_id}/prescriptions", response_model=schemas.Prescription)
async def add_prescription(patient_id: int, prescription: schemas.PrescriptionBase, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Patient).where(models.Patient.id == patient_id))
    patient = result.scalar_one_or_none()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    db_prescription = models.Prescription(patient_id=patient_id, **prescription.dict())
    db.add(db_prescription)
    await db.commit()
    await db.refresh(db_prescription)
    return db_prescription

@router.get("/{patient_id}/prescriptions", response_model=list[schemas.Prescription])
async def get_prescriptions(patient_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Prescription).where(models.Prescription.patient_id == patient_id))
    return result.scalars().all()
