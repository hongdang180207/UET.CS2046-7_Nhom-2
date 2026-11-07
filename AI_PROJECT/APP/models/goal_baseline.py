from dataclasses import dataclass


@dataclass
class GoalBaseline:
    baseline_id: int
    goal_id: int
    category_id: int
    daily_baseline_vnd: int