import pandas as pd
import numpy as np
from typing import Dict, Any, Optional

class FinanceService:

     @staticmethod
     def _prepare_df(transactions: list[Dict[str, Any]]) -> pd.DataFrame:
        "Chuyển đổi list dict từ DB sang DataFrame và chuẩn hóa kiểu dữ liệu"
        required_cols = ['amount', 'type', 'category', 'date']
        if not transactions:
            return pd.DataFrame(columns=required_cols)

        df = pd.DataFrame(transactions)

        for col in required_cols:
            if col not in df.columns:
                df[col] = np.nan

        df['date'] = pd.to_datetime(df['date'], errors='coerce')
        df['amount'] = pd.to_numeric(df['amount'], errors='coerce').fillna(0.0)
        return df.dropna(subset=['date'])

     @staticmethod
     def _filter_by_date(df,day, month, year):
         "Hàm phụ trợ lọc DataFrame theo ngày, tháng, năm bằng Boolean Mask."
         mask = pd.Series(True, index=df.index)
         if day is not None:
            mask &= (df['date'].dt.day == day)
         if month is not None:
            mask &= (df['date'].dt.month == month)
         if year is not None:
            mask &= (df['date'].dt.year == year)
         return df.loc[mask]

     @classmethod
     def calculate_total_income(cls, transactions, month, year):
        """Nhiệm vụ 1: Tính tổng thu nhập (có thể lọc theo tháng/năm)."""
        df = cls._prepare_df(transactions)
        if df.empty:
            return 0.0

        inc_df = df[df['type'] == 'income']
        filtered = cls._filter_by_date(inc_df, month=month, year=year)
        return float(filtered['amount'].sum())

     @classmethod
     def calculate_expense_by_period(cls, transactions, day, month, year ):
        "Nhiệm vụ 2: Tính tổng chi tiêu theo ngày, tháng, năm."
        df = cls._prepare_df(transactions)
        if df.empty:
            return 0.0

        exp_df = df[df['type'] == 'expense']
        filtered = cls._filter_by_date(exp_df, day=day, month=month, year=year)
        return float(filtered['amount'].sum())

     @classmethod
     def get_expense_by_category(cls, transactions, month, year):
        "Nhiệm vụ 3: Phân loại và thống kê tỷ trọng chi tiêu theo danh mục."
        df = cls._prepare_df(transactions)
        if df.empty:
            return {"total_expense": 0.0, "categories": []}

        exp_df = cls._filter_by_date(df[df['type'] == 'expense'], month=month, year=year)
        total_exp = float(exp_df['amount'].sum())

        if total_exp == 0:
            return {"total_expense": 0.0, "categories": []}

        grouped = (
            exp_df.groupby('category', as_index=False)['amount']
            .sum()
            .sort_values(by='amount', ascending=False)
        )
        grouped['percentage'] = (grouped['amount'] / total_exp * 100).round(2)

        return {
            "total_expense": round(total_exp, 2),
            "categories": grouped.to_dict(orient='records')
        }

     @classmethod
     def calculate_net_balance(cls, transactions, month, year):
        "Nhiệm vụ 4 (Gợi ý bổ sung): Tính cân đối thu chi và tỷ lệ tiết kiệm."
        total_income = cls.calculate_total_income(transactions, month=month, year=year)
        total_expense = cls.calculate_expense_by_period(transactions, month=month, year=year)
        net_savings = total_income - total_expense
        saving_rate = round((net_savings / total_income * 100), 2) if total_income > 0 else 0.0

        return {
            "total_income": round(total_income, 2),
            "total_expense": round(total_expense, 2),
            "net_balance": round(net_savings, 2),
            "saving_rate_percent": saving_rate
        }

     @classmethod
     def check_budget_status(cls, transactions, budget_limit, month, year):
        "Nhiệm vụ 5 (Gợi ý bổ sung): Kiểm tra tình trạng ngân sách tháng."
        total_expense = cls.calculate_expense_by_period(transactions, month=month, year=year)
        usage_percent = round((total_expense / budget_limit * 100), 2) if budget_limit > 0 else 0.0
        
        status = "NORMAL"
        if usage_percent >= 100:
            status = "OVER_BUDGET"
        elif usage_percent >= 80:
            status = "WARNING"

        return {
            "budget_limit": budget_limit,
            "total_expense": round(total_expense, 2),
            "remaining_budget": round(budget_limit - total_expense, 2),
            "usage_percent": usage_percent,
            "status": status
        }

     @classmethod
     def analyze_spending_trends(cls, transactions):
        "Nhiệm vụ 6: Phân tích xu hướng chi tiêu qua các tháng bằng Pandas."
        df = cls._prepare_df(transactions)
        exp_df = df[df['type'] == 'expense'].copy()
        if exp_df.empty:
            return {"monthly_trend": [], "mom_change_percent": 0.0, "trend_direction": "STABLE"}

        exp_df['year_month'] = exp_df['date'].dt.to_period('M')
        
        # Gom nhóm và điền đầy các tháng bị khuyết (nếu có tháng chi tiêu = 0)
        monthly = exp_df.groupby('year_month')['amount'].sum()
        full_period_idx = pd.period_range(start=monthly.index.min(), end=monthly.index.max(), freq='M')
        monthly = monthly.reindex(full_period_idx, fill_value=0.0).reset_index()
        monthly.columns = ['year_month', 'amount']
        monthly['year_month'] = monthly['year_month'].astype(str)

        # Tính % thay đổi liên tiếp và xử lý lỗi chia cho 0 (inf)
        pct_change = monthly['amount'].pct_change().replace([np.inf, -np.inf], np.nan).fillna(0.0)
        monthly['pct_change'] = (pct_change * 100).round(2)

        latest_change = float(monthly.iloc[-1]['pct_change']) if len(monthly) >= 2 else 0.0
        direction = "INCREASING" if latest_change > 5 else ("DECREASING" if latest_change < -5 else "STABLE")

        return {
            "monthly_trend": monthly.to_dict(orient='records'),
            "mom_change_percent": latest_change,
            "trend_direction": direction
        }