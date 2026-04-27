from __future__ import annotations

from typing import Literal, List, Optional
from pydantic import BaseModel, Field, computed_field

HomeOwnership = Literal["rent", "own", "mortgage", "family"]
EmploymentType = Literal["full_time", "part_time", "self_employed", "contract", "unemployed"]
LoanPurpose = Literal["personal", "business", "education", "home", "vehicle", "medical", "debt_consolidation"]
CollateralType = Literal["none", "vehicle", "real_estate", "savings", "guarantor"]


class CustomerInput(BaseModel):
    full_name: str = Field(default="Khách hàng mới", min_length=1, max_length=120)
    age: int = Field(ge=18, le=80)
    monthly_income: float = Field(gt=0)
    loan_amount: float = Field(gt=0)
    loan_term_months: int = Field(ge=1, le=360)
    credit_history_years: float = Field(ge=0, le=60)
    late_payments_12m: int = Field(ge=0, le=24)
    existing_debt: float = Field(ge=0)
    num_credit_cards: int = Field(ge=0, le=20)
    credit_utilization: float = Field(ge=0, le=1, description="Tỷ lệ sử dụng hạn mức thẻ, 0-1")
    employment_years: float = Field(ge=0, le=60)
    employment_type: EmploymentType
    home_ownership: HomeOwnership
    loan_purpose: LoanPurpose
    collateral_type: CollateralType
    number_of_dependents: int = Field(ge=0, le=15)
    recent_credit_inquiries: int = Field(ge=0, le=20)

    @computed_field
    @property
    def annual_income(self) -> float:
        return self.monthly_income * 12


class Reason(BaseModel):
    factor: str
    impact: Literal["risk_increase", "risk_decrease", "neutral"]
    message: str
    severity: Literal["low", "medium", "high"]


class ScoreResult(BaseModel):
    customer_name: str
    probability_default: float
    credit_score: int
    rating: str
    decision: str
    risk_level: str
    engineered_features: dict
    main_reasons: List[Reason]
    recommendation: str


class ApiResponse(BaseModel):
    success: bool = True
    data: ScoreResult
    message: Optional[str] = None
