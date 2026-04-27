from __future__ import annotations

import numpy as np
import pandas as pd
from pathlib import Path

EMPLOYMENT_TYPES = ["full_time", "part_time", "self_employed", "contract", "unemployed"]
HOME_OWNERSHIP = ["rent", "own", "mortgage", "family"]
LOAN_PURPOSES = ["personal", "business", "education", "home", "vehicle", "medical", "debt_consolidation"]
COLLATERAL_TYPES = ["none", "vehicle", "real_estate", "savings", "guarantor"]


def generate_credit_data(n: int = 12000, random_state: int = 42) -> pd.DataFrame:
    rng = np.random.default_rng(random_state)

    age = rng.integers(18, 75, n)
    monthly_income = rng.lognormal(mean=np.log(18_000_000), sigma=0.65, size=n).clip(4_000_000, 150_000_000).round(0)
    loan_amount = rng.lognormal(mean=np.log(90_000_000), sigma=0.85, size=n).clip(5_000_000, 1_500_000_000).round(0)
    loan_term_months = rng.choice([6, 12, 18, 24, 36, 48, 60, 84, 120], n, p=[0.06, 0.15, 0.08, 0.22, 0.18, 0.12, 0.12, 0.04, 0.03])
    credit_history_years = rng.integers(0, 25, n) + rng.random(n)
    late_payments_12m = rng.poisson(lam=0.8, size=n).clip(0, 12)
    existing_debt = rng.lognormal(mean=np.log(35_000_000), sigma=1.0, size=n).clip(0, 700_000_000).round(0)
    num_credit_cards = rng.integers(0, 9, n)
    credit_utilization = rng.beta(2.0, 3.2, n).clip(0, 1)
    employment_years = rng.integers(0, 30, n) + rng.random(n)
    number_of_dependents = rng.choice([0, 1, 2, 3, 4, 5], n, p=[0.32, 0.22, 0.24, 0.14, 0.06, 0.02])
    recent_credit_inquiries = rng.poisson(lam=1.2, size=n).clip(0, 12)

    employment_type = rng.choice(EMPLOYMENT_TYPES, n, p=[0.58, 0.10, 0.18, 0.10, 0.04])
    home_ownership = rng.choice(HOME_OWNERSHIP, n, p=[0.42, 0.25, 0.18, 0.15])
    loan_purpose = rng.choice(LOAN_PURPOSES, n, p=[0.28, 0.18, 0.10, 0.10, 0.14, 0.08, 0.12])
    collateral_type = rng.choice(COLLATERAL_TYPES, n, p=[0.48, 0.20, 0.12, 0.10, 0.10])

    annual_income = monthly_income * 12
    debt_to_income = existing_debt / np.maximum(annual_income, 1)
    loan_to_income = loan_amount / np.maximum(annual_income, 1)
    installment_to_income = (loan_amount / np.maximum(loan_term_months, 1)) / np.maximum(monthly_income, 1)

    risk = (
        -2.0
        + 1.45 * debt_to_income
        + 0.75 * loan_to_income
        + 1.10 * installment_to_income
        + 0.38 * late_payments_12m
        + 1.10 * credit_utilization
        + 0.18 * recent_credit_inquiries
        - 0.08 * credit_history_years
        - 0.045 * employment_years
        - 0.012 * age
        + 0.10 * number_of_dependents
    )

    risk += np.where(employment_type == "unemployed", 1.2, 0)
    risk += np.where(employment_type == "contract", 0.35, 0)
    risk += np.where(employment_type == "self_employed", 0.25, 0)
    risk += np.where(home_ownership == "own", -0.35, 0)
    risk += np.where(home_ownership == "mortgage", -0.15, 0)
    risk += np.where(collateral_type == "real_estate", -0.45, 0)
    risk += np.where(collateral_type == "savings", -0.35, 0)
    risk += np.where(collateral_type == "none", 0.15, 0)
    risk += np.where(loan_purpose == "debt_consolidation", 0.30, 0)
    risk += np.where(loan_purpose == "business", 0.20, 0)
    risk += rng.normal(0, 0.8, n)

    probability_default = 1 / (1 + np.exp(-risk))
    default = (rng.random(n) < probability_default).astype(int)

    df = pd.DataFrame({
        "full_name": [f"KH_{i:05d}" for i in range(n)],
        "age": age,
        "monthly_income": monthly_income,
        "loan_amount": loan_amount,
        "loan_term_months": loan_term_months,
        "credit_history_years": np.round(credit_history_years, 2),
        "late_payments_12m": late_payments_12m,
        "existing_debt": existing_debt,
        "num_credit_cards": num_credit_cards,
        "credit_utilization": np.round(credit_utilization, 3),
        "employment_years": np.round(employment_years, 2),
        "employment_type": employment_type,
        "home_ownership": home_ownership,
        "loan_purpose": loan_purpose,
        "collateral_type": collateral_type,
        "number_of_dependents": number_of_dependents,
        "recent_credit_inquiries": recent_credit_inquiries,
        "default": default,
    })

    return df


def ensure_dataset(path: str | Path, n: int = 12000) -> pd.DataFrame:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        return pd.read_csv(path)
    df = generate_credit_data(n=n)
    df.to_csv(path, index=False)
    return df
