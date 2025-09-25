from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from app.core.db import Base
import datetime

class Patient(Base):
    __tablename__ = "patients"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    birth_date = Column(String, nullable=True)
    prescriptions = relationship("Prescription", back_populates="patient", cascade="all, delete")

class Prescription(Base):
    __tablename__ = "prescriptions"
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id", ondelete="CASCADE"))
    drug_name = Column(String, nullable=False)
    dosage = Column(String, nullable=False)
    patient = relationship("Patient", back_populates="prescriptions")
    intakes = relationship("Intake", back_populates="prescription", cascade="all, delete")

class Intake(Base):
    __tablename__ = "intakes"
    id = Column(Integer, primary_key=True, index=True)
    prescription_id = Column(Integer, ForeignKey("prescriptions.id", ondelete="CASCADE"))
    taken_at = Column(DateTime, default=datetime.datetime.utcnow)
    taken = Column(Boolean, default=False)
    prescription = relationship("Prescription", back_populates="intakes")
