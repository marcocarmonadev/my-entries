import datetime as dt
from enum import Enum
from uuid import UUID, uuid4

from dateutil.relativedelta import relativedelta
from pydantic import BaseModel
from pydantic.fields import Field
from sqlalchemy.orm import Mapped, mapped_column

from . import Base


class Status(Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    CLOSED = "closed"


class Frequency(Enum):
    ONE_TIME = "one-time"
    WEEKLY = "weekly"
    BI_WEEKLY = "bi-weekly"
    MONTLY = "montly"
    YEARLY = "yearly"


class UpdateSchema(BaseModel):
    concept: str | None = Field(
        default=None,
    )
    amount: float | None = Field(
        default=None,
    )
    due_date: dt.date | None = Field(
        default=None,
    )
    status: Status | None = Field(
        default=None,
    )


class ReadSchema(BaseModel):
    concept: str
    amount: float
    creation_date: dt.datetime
    due_date: dt.date
    uuid: UUID
    repeat_forever: bool
    status: Status
    frequency: Frequency
    repeated: bool


class CreateSchema(BaseModel):
    concept: str
    amount: float
    due_date: dt.date
    status: Status = Field(
        default=Status.PENDING,
    )
    frequency: Frequency = Field(
        default=Frequency.ONE_TIME,
    )
    repeat_count: int = Field(
        default=1,
        ge=0,
    )
    repeat_interval: int = Field(
        default=1,
        ge=1,
    )


class UpdateAmountInsideCajita(BaseModel):
    new_amount: float


class Model(Base):
    __tablename__ = "entries"

    id: Mapped[int] = mapped_column(
        primary_key=True,
    )
    concept: Mapped[str]
    amount: Mapped[float]
    due_date: Mapped[dt.date]
    status: Mapped[Status]
    frequency: Mapped[Frequency]
    creation_date: Mapped[dt.datetime] = mapped_column(
        default=dt.datetime.now,
    )
    uuid: Mapped[UUID] = mapped_column(
        default=uuid4,
    )
    repeat_interval: Mapped[int | None] = mapped_column(
        default=None,
    )
    repeated: Mapped[bool] = mapped_column(
        default=False,
    )
    repeat_forever: Mapped[bool] = mapped_column(
        default=False,
    )


def get_nearest_fortnight_date(
    date: dt.date,
):
    if date.day <= 15:
        return date + relativedelta(
            day=15,
        )
    else:
        return date + relativedelta(
            day=30,
        )


def get_next_nearest_fortnight_date(
    date: dt.date,
):
    if date.day == 15:
        return date + relativedelta(
            day=30,
        )
    else:
        return date + relativedelta(
            months=1,
            day=15,
        )


def get_next_due_date(
    date: dt.date,
    frequency: Frequency,
    repeat_interval: int | None,
):
    match frequency:
        case Frequency.ONE_TIME:
            raise
        case Frequency.BI_WEEKLY:
            next_due_date = get_next_nearest_fortnight_date(date)
        case Frequency.WEEKLY:
            next_due_date = date + relativedelta(
                weeks=repeat_interval,
            )
        case Frequency.MONTLY:
            next_due_date = date + relativedelta(
                months=repeat_interval,
            )
        case Frequency.YEARLY:
            next_due_date = date + relativedelta(
                years=repeat_interval,
            )
    return next_due_date
