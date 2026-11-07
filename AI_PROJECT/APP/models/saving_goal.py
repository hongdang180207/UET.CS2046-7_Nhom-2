from dataclasses import dataclass
from datetime import date, datetime
from typing import Literal


GoalStatus = Literal["active", "completed", "paused", "cancelled"]


@dataclass
class SavingGoal:
    goal_id: int
    user_id: int
    name: str
    target_amount_vnd: int
    deadline: date
    status: GoalStatus
    created_at: datetime