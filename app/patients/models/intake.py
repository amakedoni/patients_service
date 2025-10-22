from sqlalchemy import Column, Integer, ForeignKey, TIMESTAMP, Boolean, Float, Time
from sqlalchemy.sql import func
from app.db.base import Base

class IntakeHistory(Base):
    __tablename__ = "intake_history"

    id = Column(Integer, primary_key=True, index=True)
    medicine_id = Column(Integer, ForeignKey("medicines.id", ondelete="CASCADE"), nullable=False)
    patient_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    planned_time = Column(Time)
    datetime = Column(TIMESTAMP(timezone=True))
    taken = Column(Boolean, default=False)
    skipped = Column(Boolean, default=False)
    dose_taken = Column(Float)
    synced = Column(Boolean, server_default="false")
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
