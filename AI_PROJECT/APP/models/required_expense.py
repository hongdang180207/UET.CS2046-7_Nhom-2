from dataclasses import dataclass
from datetime import date
from typing import Literal


ExpenseStatus = Literal["unpaid", "paid", "cancelled"]


@dataclass
class RequiredExpense:
    expense_id: int
    user_id: int
    name: str
    amount_vnd: int
    due_date: date
    status: ExpenseStatus
    paid_transaction_id: int | None