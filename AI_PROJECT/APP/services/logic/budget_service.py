from typing import Any
from services.finance_service import FinanceService


class BudgetService:
    @staticmethod
    def evaluate_category_budget(
        category: str,
        budget_limit: float,
        spent_amount: float,
        warning_threshold: float = 80.0,
    ) -> dict[str, Any]:

        if budget_limit < 0 or spent_amount < 0:
            raise ValueError("Hạn mức ngân sách và số tiền chi tiêu không được âm.")

        remaining = budget_limit - spent_amount

        if budget_limit > 0:
            usage_percent = round((spent_amount / budget_limit) * 100, 2)
        else:
            usage_percent = 100.0 if spent_amount > 0 else 0.0

        if spent_amount > budget_limit:
            status = "EXCEEDED"
            alert_msg = (
                f"Cảnh báo: Danh mục '{category}' đã vượt ngân sách "
                f"{abs(remaining):,.0f} VNĐ ({usage_percent}%)."
            )
        elif usage_percent >= warning_threshold:
            status = "WARNING"
            alert_msg = (
                f"Lưu ý: Danh mục '{category}' đã dùng {usage_percent}% ngân sách. "
                f"Chỉ còn {remaining:,.0f} VNĐ."
            )
        else:
            status = "SAFE"
            alert_msg = (
                f"Danh mục '{category}' đang trong tầm kiểm soát "
                f"(Còn lại {remaining:,.0f} VNĐ)."
            )

        return {
            "category": category,
            "budget_limit": budget_limit,
            "spent_amount": spent_amount,
            "remaining_amount": remaining,
            "usage_percentage": usage_percent,
            "status": status,
            "alert_message": alert_msg,
        }

    @classmethod
    def check_all_budgets(
        cls,
        transactions: list[dict[str, Any]],
        budgets: dict[str, float],
        month: int,
        year: int,
        warning_threshold: float = 80.0,
    ) -> list[dict[str, Any]]:
       
        cat_summary = FinanceService.get_expense_by_category(transactions, month, year)
        spent_map = {
            item["category"]: item["amount"]
            for item in cat_summary.get("categories", [])
        }

        results = []
        for category, limit in budgets.items():
            spent = spent_map.get(category, 0.0)
            results.append(
                cls.evaluate_category_budget(
                    category=category,
                    budget_limit=limit,
                    spent_amount=spent,
                    warning_threshold=warning_threshold,
                )
            )

        return results