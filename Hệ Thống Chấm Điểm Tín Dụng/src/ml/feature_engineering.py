from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin


class CreditFeatureEngineer(BaseEstimator, TransformerMixin):
    """Tạo các biến tài chính có ý nghĩa nghiệp vụ trước khi train/predict.

    Transformer này dùng được trong sklearn Pipeline để đảm bảo train và predict
    đi qua cùng một quy trình xử lý dữ liệu.
    """

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        df = pd.DataFrame(X).copy()

        monthly_income = df["monthly_income"].astype(float).clip(lower=1)
        annual_income = monthly_income * 12
        loan_amount = df["loan_amount"].astype(float)
        existing_debt = df["existing_debt"].astype(float)
        term = df["loan_term_months"].astype(float).clip(lower=1)
        dependents = df["number_of_dependents"].astype(float)

        # Ước lượng trả góp theo tháng chưa tính lãi phức tạp để dễ giải thích.
        estimated_monthly_installment = loan_amount / term

        df["debt_to_income"] = existing_debt / annual_income
        df["loan_to_income"] = loan_amount / annual_income
        df["installment_to_income"] = estimated_monthly_installment / monthly_income
        df["income_per_dependent"] = monthly_income / (dependents + 1)
        df["credit_history_age_ratio"] = df["credit_history_years"].astype(float) / np.maximum(df["age"].astype(float), 1)
        df["has_collateral"] = (df["collateral_type"].astype(str) != "none").astype(int)
        df["late_payment_flag"] = (df["late_payments_12m"].astype(float) > 0).astype(int)
        df["high_utilization_flag"] = (df["credit_utilization"].astype(float) >= 0.7).astype(int)

        return df


ENGINEERED_NUMERIC_FEATURES = [
    "debt_to_income",
    "loan_to_income",
    "installment_to_income",
    "income_per_dependent",
    "credit_history_age_ratio",
    "has_collateral",
    "late_payment_flag",
    "high_utilization_flag",
]

BASE_NUMERIC_FEATURES = [
    "age",
    "monthly_income",
    "loan_amount",
    "loan_term_months",
    "credit_history_years",
    "late_payments_12m",
    "existing_debt",
    "num_credit_cards",
    "credit_utilization",
    "employment_years",
    "number_of_dependents",
    "recent_credit_inquiries",
]

CATEGORICAL_FEATURES = [
    "employment_type",
    "home_ownership",
    "loan_purpose",
    "collateral_type",
]

MODEL_NUMERIC_FEATURES = BASE_NUMERIC_FEATURES + ENGINEERED_NUMERIC_FEATURES
ALL_MODEL_FEATURES = MODEL_NUMERIC_FEATURES + CATEGORICAL_FEATURES


def compute_engineered_features_for_display(customer: dict) -> dict:
    df = CreditFeatureEngineer().transform(pd.DataFrame([customer]))
    values = df.iloc[0]
    keys = [
        "debt_to_income",
        "loan_to_income",
        "installment_to_income",
        "income_per_dependent",
        "credit_history_age_ratio",
        "has_collateral",
        "late_payment_flag",
        "high_utilization_flag",
    ]
    return {k: round(float(values[k]), 4) for k in keys}
