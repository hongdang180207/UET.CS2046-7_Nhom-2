from datetime import datetime
from typing import Dict, Any

class SavingService:
    @staticmethod
    def evaluate_saving_goal(goal_name: str, target_amount: float, current_saved: float, deadline_str: str) -> Dict[str, Any]:
        """
        Theo dõi mục tiêu tiết kiệm.
        deadline_str format: 'YYYY-MM-DD'
        """
        remaining_amount = max(0.0, target_amount - current_saved)
        progress_percent = round((current_saved / target_amount) * 100, 2) if target_amount > 0 else 100.0

        today = datetime.now().date()
        deadline = datetime.strptime(deadline_str, "%Y-%m-%d").date()
        days_left = (deadline - today).days

        if remaining_amount == 0:
            status = "COMPLETED"
            daily_needed = 0.0
            monthly_needed = 0.0
        elif days_left <= 0:
            status = "OVERDUE"
            daily_needed = remaining_amount
            monthly_needed = remaining_amount
        else:
            status = "IN_PROGRESS"
            daily_needed = round(remaining_amount / days_left, 0)
            months_left = max(1.0, days_left / 30.0)
            monthly_needed = round(remaining_amount / months_left, 0)

        return {
            "goal_name": goal_name,
            "target_amount": target_amount,
            "current_saved": current_saved,
            "remaining_amount": remaining_amount,
            "progress_percentage": progress_percent,
            "days_remaining": max(0, days_left),
            "required_per_day": daily_needed,
            "required_per_month": monthly_needed,
            "status": status
        }