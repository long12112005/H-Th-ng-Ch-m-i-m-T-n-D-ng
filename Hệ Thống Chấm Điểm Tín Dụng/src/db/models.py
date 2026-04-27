from __future__ import annotations

from datetime import datetime
from sqlalchemy import DateTime, Float, Integer, String, Text, JSON
from sqlalchemy.orm import Mapped, mapped_column

from src.db.database import Base


class ScoreApplication(Base):
    __tablename__ = "score_applications"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, index=True)
    customer_name: Mapped[str] = mapped_column(String(120), index=True)

    age: Mapped[int] = mapped_column(Integer)
    monthly_income: Mapped[float] = mapped_column(Float)
    loan_amount: Mapped[float] = mapped_column(Float)
    loan_term_months: Mapped[int] = mapped_column(Integer)
    credit_history_years: Mapped[float] = mapped_column(Float)
    late_payments_12m: Mapped[int] = mapped_column(Integer)
    existing_debt: Mapped[float] = mapped_column(Float)
    num_credit_cards: Mapped[int] = mapped_column(Integer)
    credit_utilization: Mapped[float] = mapped_column(Float)
    employment_years: Mapped[float] = mapped_column(Float)
    employment_type: Mapped[str] = mapped_column(String(40))
    home_ownership: Mapped[str] = mapped_column(String(40))
    loan_purpose: Mapped[str] = mapped_column(String(40))
    collateral_type: Mapped[str] = mapped_column(String(40))
    number_of_dependents: Mapped[int] = mapped_column(Integer)
    recent_credit_inquiries: Mapped[int] = mapped_column(Integer)

    probability_default: Mapped[float] = mapped_column(Float)
    credit_score: Mapped[int] = mapped_column(Integer, index=True)
    rating: Mapped[str] = mapped_column(String(40))
    decision: Mapped[str] = mapped_column(String(80), index=True)
    risk_level: Mapped[str] = mapped_column(String(40), index=True)
    engineered_features: Mapped[dict] = mapped_column(JSON)
    main_reasons: Mapped[list] = mapped_column(JSON)
    recommendation: Mapped[str] = mapped_column(Text)


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, index=True)
    action: Mapped[str] = mapped_column(String(80), index=True)
    detail: Mapped[str] = mapped_column(Text)
