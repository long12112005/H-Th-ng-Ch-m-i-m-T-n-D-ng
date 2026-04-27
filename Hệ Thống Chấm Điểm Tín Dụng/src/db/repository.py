from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.core.schemas import CustomerInput, ScoreResult
from src.db.models import ScoreApplication, AuditLog


def save_score_application(session: Session, customer: CustomerInput, result: ScoreResult) -> ScoreApplication:
    customer_data = customer.model_dump()
    row = ScoreApplication(
        customer_name=customer.full_name,
        age=customer.age,
        monthly_income=customer.monthly_income,
        loan_amount=customer.loan_amount,
        loan_term_months=customer.loan_term_months,
        credit_history_years=customer.credit_history_years,
        late_payments_12m=customer.late_payments_12m,
        existing_debt=customer.existing_debt,
        num_credit_cards=customer.num_credit_cards,
        credit_utilization=customer.credit_utilization,
        employment_years=customer.employment_years,
        employment_type=customer.employment_type,
        home_ownership=customer.home_ownership,
        loan_purpose=customer.loan_purpose,
        collateral_type=customer.collateral_type,
        number_of_dependents=customer.number_of_dependents,
        recent_credit_inquiries=customer.recent_credit_inquiries,
        probability_default=result.probability_default,
        credit_score=result.credit_score,
        rating=result.rating,
        decision=result.decision,
        risk_level=result.risk_level,
        engineered_features=result.engineered_features,
        main_reasons=[r.model_dump() for r in result.main_reasons],
        recommendation=result.recommendation,
    )
    session.add(row)
    session.add(AuditLog(action="score_customer", detail=f"Scored customer: {customer_data.get('full_name')}"))
    session.commit()
    session.refresh(row)
    return row


def list_applications(session: Session, limit: int = 50) -> list[ScoreApplication]:
    stmt = select(ScoreApplication).order_by(ScoreApplication.created_at.desc()).limit(limit)
    return list(session.execute(stmt).scalars().all())


def list_audit_logs(session: Session, limit: int = 100) -> list[AuditLog]:
    stmt = select(AuditLog).order_by(AuditLog.created_at.desc()).limit(limit)
    return list(session.execute(stmt).scalars().all())
