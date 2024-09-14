import datetime as dt
from enum import StrEnum
from uuid import UUID

from pydantic import BaseModel


class Status(StrEnum):
    PENDING = "pending"
    COMPLETED = "completed"
    GENERATE_INVOICE = "generate_invoice"
    WAITING_INVOICE = "waiting_invoice"
    CLOSED = "closed"


class Entry(BaseModel):
    concept: str
    amount: float
    due_date: dt.date
    uuid: UUID
    status: Status
