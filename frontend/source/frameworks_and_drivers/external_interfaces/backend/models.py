import datetime as dt
from enum import StrEnum
from uuid import UUID

from pydantic import BaseModel


class Status(StrEnum):
    PENDING = "pending"
    COMPLETED = "completed"
    CLOSED = "closed"


class Frequency(StrEnum):
    ONE_TIME = "one-time"
    WEEKLY = "weekly"
    BI_WEEKLY = "bi-weekly"
    MONTLY = "montly"
    YEARLY = "yearly"


class Entry(BaseModel):
    concept: str
    amount: float
    due_date: dt.date
    uuid: UUID
    status: Status
    frequency: Frequency
