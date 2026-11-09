from datetime import datetime, date
import math
from typing import Dict, Any

class SavingService:
    @staticmethod
    def evaluate_saving_goal(
        goal_name: str, 
        target_amount: float, 
        current_saved: float, 
        deadline_str: str,
        current_date: date | None = None
    ) -> Dict[str, Any]:
        """
        Đánh giá và theo dõi tiến độ mục tiêu tiết kiệm.
        :param deadline_str: Định dạng 'YYYY-MM-DD'
        :param current_date: Tùy chọn truyền ngày để dễ viết unit test.
        """
        try:
            deadline = datetime.strptime(deadline_str, "%Y-%m-%d").date()
        except ValueError as err:
            raise ValueError(f"Định dạng ngày không hợp lệ (cần YYYY-MM-DD): {deadline_str}") from err

        today = current_date or datetime.now().date()
        days_left = (deadline - today).days

        remaining_amount = max(0.0, target_amount - current_saved)
        
        # Tính phần trăm hoàn thành (giới hạn 0 - 100 hoặc giữ thực tế tùy mục đích)
        if target_amount <= 0:
            progress_percent = 100.0
        else:
            progress_percent = round((current_saved / target_amount) * 100, 2)

        if remaining_amount == 0.0:
            status = "COMPLETED"
            daily_needed = 0.0
            monthly_needed = 0.0
        elif days_left < 0:
            status = "OVERDUE"
            daily_needed = remaining_amount
            monthly_needed = remaining_amount
        else:
            # Bao gồm cả ngày hôm nay (nếu days_left == 0 thì còn 1 ngày cuối để tích luỹ)
            status = "IN_PROGRESS"
            effective_days = max(1, days_left)
            
            # Làm tròn lên để tránh bị hụt số tiền khi tiết kiệm hàng ngày/tháng
            daily_needed = float(math.ceil(remaining_amount / effective_days))
            
            # Ước tính theo tháng (30 ngày/tháng)
            months_left = effective_days / 30.0
            monthly_needed = float(math.ceil(remaining_amount / months_left)) if months_left > 0 else remaining_amount

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