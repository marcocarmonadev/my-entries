from pydantic import BaseModel


class StatisticsSchema(BaseModel):
    total_amount: float
    income_amount: float
    expense_amount: float
