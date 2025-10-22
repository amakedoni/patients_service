import enum
from sqlalchemy import (
    Column, Integer, Date, Enum, ARRAY, Time, TIMESTAMP, CheckConstraint
)
from sqlalchemy.sql import func
from app.db.base import Base

class ScheduleType(str, enum.Enum):
    daily = "daily"
    weekly_days = "weekly_days"
    cycle = "cycle"
    every_x_days = "every_x_days"

class Schedule(Base):
    __tablename__ = "schedules"

    id = Column(Integer, primary_key=True, index=True)
    start_date = Column(Date, nullable=False)
    duration_days = Column(Integer, default=0)
    schedule_type = Column(Enum(ScheduleType), nullable=False)
    days_of_week = Column(ARRAY(Integer))
    cycle_on = Column(Integer)
    cycle_off = Column(Integer)
    every_x_days = Column(Integer)
    every_x_weeks = Column(Integer)
    times_per_day = Column(Integer, nullable=False)
    time_list = Column(ARRAY(Time))
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())

    __table_args__ = (
        CheckConstraint("times_per_day <= 6", name="max_times_per_day"),
        CheckConstraint("duration_days <= 3650", name="max_duration_days"),
        CheckConstraint("cycle_on <= 60", name="max_cycle_on"),
        CheckConstraint("cycle_off <= 60", name="max_cycle_off"),
        CheckConstraint("every_x_days <= 30", name="max_every_x_days"),
    )
