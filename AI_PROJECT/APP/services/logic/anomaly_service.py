import pandas as pd
import numpy as np
from typing import Dict, Any, List
from services.logic import finance_service


class AnomalyService:
    @staticmethod
    def detect_unusual_transactions(
        transactions: List[Dict[str, Any]], 
        z_threshold: float = 2.0,
        multiplier_threshold: float = 3.0,
        min_category_count: int = 3
    ) -> List[Dict[str, Any]]:
        """
        Phát hiện giao dịch bất thường (lớn đột biến so với mức trung bình của chính danh mục đó).
        Sử dụng kết hợp Z-score và ngưỡng gấp N lần trung bình.
        """
        if not transactions:
            return []

        df = finance_service._prepare_df(transactions)
        if df.empty or 'type' not in df.columns:
            return []

        exp_df = df.loc[df['type'] == 'expense'].copy()
        if len(exp_df) < 5:
            return []


        grouped = exp_df.groupby('category')['amount']
        exp_df['cat_count'] = grouped.transform('count')
        exp_df['mean'] = grouped.transform('mean')
        exp_df['std'] = grouped.transform('std').fillna(0)


        exp_df['z_score'] = np.where(
            exp_df['std'] > 0,
            (exp_df['amount'] - exp_df['mean']) / exp_df['std'],
            0.0
        )