from __future__ import annotations

import joblib
import pandas as pd

from src.core.config import settings
from src.core.schemas import CustomerInput, ScoreResult
from src.core.scoring import (
    probability_to_credit_score,
    get_credit_rating,
    get_decision,
    get_risk_level,
    get_recommendation,
)
from src.ml.feature_engineering import compute_engineered_features_for_display
from src.ml.reasoner import build_reasons
from src.ml.training import train_and_save


def load_model(auto_train: bool = True):
    if not settings.model_path.exists():
        if not auto_train:
            raise FileNotFoundError(f"Chưa có model tại {settings.model_path}. Hãy chạy python src/train.py trước.")
        train_and_save()
    return joblib.load(settings.model_path)


def score_customer(customer: CustomerInput | dict, auto_train: bool = True) -> ScoreResult:
    if isinstance(customer, CustomerInput):
        customer_obj = customer
    else:
        customer_obj = CustomerInput(**customer)

    customer_dict = customer_obj.model_dump()
    model = load_model(auto_train=auto_train)

    X = pd.DataFrame([customer_dict]).drop(columns=["full_name"], errors="ignore")
    probability_default = float(model.predict_proba(X)[0][1])
    credit_score = probability_to_credit_score(probability_default, settings.min_credit_score, settings.max_credit_score)
    rating = get_credit_rating(credit_score)
    decision = get_decision(credit_score, probability_default)
    risk_level = get_risk_level(probability_default)
    engineered = compute_engineered_features_for_display(customer_dict)
    reasons = build_reasons(customer_dict, engineered)
    recommendation = get_recommendation(credit_score, probability_default)

    return ScoreResult(
        customer_name=customer_obj.full_name,
        probability_default=round(probability_default, 4),
        credit_score=credit_score,
        rating=rating,
        decision=decision,
        risk_level=risk_level,
        engineered_features=engineered,
        main_reasons=reasons,
        recommendation=recommendation,
    )
