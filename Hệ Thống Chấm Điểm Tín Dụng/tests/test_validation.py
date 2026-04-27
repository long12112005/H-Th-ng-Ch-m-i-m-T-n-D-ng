import pytest
from pydantic import ValidationError
from src.core.schemas import CustomerInput


def base_customer():
    return {
        "full_name": "Test",
        "age": 30,
        "monthly_income": 20000000,
        "loan_amount": 100000000,
        "loan_term_months": 24,
        "credit_history_years": 4,
        "late_payments_12m": 0,
        "existing_debt": 20000000,
        "num_credit_cards": 2,
        "credit_utilization": 0.35,
        "employment_years": 3,
        "employment_type": "full_time",
        "home_ownership": "rent",
        "loan_purpose": "personal",
        "collateral_type": "none",
        "number_of_dependents": 1,
        "recent_credit_inquiries": 1,
    }


def test_invalid_age():
    data = base_customer()
    data["age"] = 12
    with pytest.raises(ValidationError):
        CustomerInput(**data)
