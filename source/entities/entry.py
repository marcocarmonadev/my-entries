import datetime as dt
from enum import Enum
from uuid import UUID, uuid4

from pydantic import BaseModel
from pydantic.fields import Field
from sqlalchemy.orm import Mapped, mapped_column

from . import Base


class Status(Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    GENERATE_INVOICE = "generate_invoice"
    WAITING_INVOICE = "waiting_invoice"
    CLOSED = "closed"


class CreateSchema(BaseModel):
    concept: str
    amount: float
    due_date: dt.date
    status: Status
    repeat_count: int = Field(
        default=0,
        ge=-1,
    )
    repeat_interval: int = Field(
        default=1,
        ge=1,
    )


class UpdateStatusSchema(BaseModel):
    status: Status


class ReadSchema(BaseModel):
    concept: str
    amount: float
    creation_date: dt.datetime
    due_date: dt.date
    uuid: UUID
    repeat_forever: bool
    status: Status
    repeated: bool | None


class Model(Base):
    __tablename__ = "entries"

    id: Mapped[int] = mapped_column(
        primary_key=True,
    )
    concept: Mapped[str]
    amount: Mapped[float]
    creation_date: Mapped[dt.datetime] = mapped_column(
        default=dt.datetime.now,
    )
    due_date: Mapped[dt.date]
    uuid: Mapped[UUID] = mapped_column(
        default=uuid4,
    )
    status: Mapped[Status]
    repeat_forever: Mapped[bool]
    repeated: Mapped[bool | None] = mapped_column(
        default=None,
    )
    repeat_interval: Mapped[int | None] = mapped_column(
        default=None,
    )
