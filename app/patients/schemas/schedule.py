from pydantic import BaseModel
from typing import List, Optional
from datetime import date, time, datetime
from enum import Enum

class ScheduleType(str, Enum):
    daily = "daily"
    weekly_days = "weekly_days"
    cycle = "cycle"
    every_x_days = "every_x_days"

class ScheduleCreate(BaseModel):
    start_date: date
    duration_days: int = 0
    schedule_type: ScheduleType
    days_of_week: Optional[List[int]] = None
    cycle_on: Optional[int] = None
    cycle_off: Optional[int] = None
    every_x_days: Optional[int] = None
    every_x_weeks: Optional[int] = None
    times_per_day: int
    time_list: Optional[List[time]] = None

class ScheduleOut(ScheduleCreate):
    id: int
    created_at: Optional[datetime] = None  # Изменено с str на datetime

    class Config:
        from_attributes = True  # Вместо orm_mode = True
