from sqlalchemy.orm import declarative_base

Base = declarative_base()

from app.patients.models.user import User  # noqa
from app.patients.models.relation import UserRelation  # noqa
from app.patients.models.schedule import Schedule  # noqa
from app.patients.models.medicine import Medicine  # noqa
from app.patients.models.intake import IntakeHistory  # noqa
