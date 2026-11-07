from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal


@dataclass
class BudgetSettings:
    setting_id: int
    user_id: int
    monthly_budget_vnd: int
    payday: int | None
    reserve_rate: Decimal
    updated_at: datetime