import enum
from sqlalchemy import Column, Integer, String, Text, Enum, Float, ForeignKey, TIMESTAMP
from sqlalchemy.sql import func
from app.db.base import Base

class MedicineForm(str, enum.Enum):
    tablet = "tablet"
    drop = "drop"
    spray = "spray"
    solution = "solution"
    injection = "injection"
    powder = "powder"
    inhaler = "inhaler"
    other = "other"

class MedicineUnit(str, enum.Enum):
    mg = "mg"
    g = "g"
    pcs = "pcs"
    ml = "ml"
    caps = "caps."
    dose = "dose"

class Medicine(Base):
    __tablename__ = "medicines"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    schedules_id = Column(Integer, ForeignKey("schedules.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(255), nullable=False)
    form = Column(Enum(MedicineForm), nullable=False)
    unit = Column(Enum(MedicineUnit), nullable=False)
    dosage = Column(Float, nullable=False)
    instructions = Column(Text)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
