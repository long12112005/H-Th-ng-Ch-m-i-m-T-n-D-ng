from __future__ import annotations

from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from src.core.config import settings
from src.core.schemas import CustomerInput, ApiResponse
from src.ml.predictor import score_customer
from src.ml.training import load_metrics, train_and_save
from src.db.database import get_session, init_db
from src.db.repository import save_score_application, list_applications, list_audit_logs

app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
    description="API cho hệ thống chấm điểm tín dụng dùng Machine Learning.",
)


@app.on_event("startup")
def startup() -> None:
    init_db()


@app.get("/health")
def health_check() -> dict:
    return {"status": "ok", "app": settings.app_name}


@app.get("/api/v1/model/metrics")
def model_metrics() -> dict:
    return load_metrics()


@app.post("/api/v1/score", response_model=ApiResponse)
def score(customer: CustomerInput, session: Session = Depends(get_session)) -> ApiResponse:
    result = score_customer(customer)
    save_score_application(session, customer, result)
    return ApiResponse(success=True, data=result, message="Chấm điểm thành công")


@app.get("/api/v1/applications")
def applications(limit: int = 50, session: Session = Depends(get_session)) -> list[dict]:
    rows = list_applications(session, limit=limit)
    return [
        {
            "id": r.id,
            "created_at": r.created_at.isoformat(),
            "customer_name": r.customer_name,
            "credit_score": r.credit_score,
            "probability_default": r.probability_default,
            "rating": r.rating,
            "decision": r.decision,
            "risk_level": r.risk_level,
        }
        for r in rows
    ]


@app.get("/api/v1/audit-logs")
def audit_logs(limit: int = 100, session: Session = Depends(get_session)) -> list[dict]:
    rows = list_audit_logs(session, limit=limit)
    return [
        {"id": r.id, "created_at": r.created_at.isoformat(), "action": r.action, "detail": r.detail}
        for r in rows
    ]


@app.post("/api/v1/model/retrain")
def retrain_model() -> dict:
    metrics = train_and_save()
    return {"success": True, "message": "Train lại mô hình thành công", "metrics": metrics}
