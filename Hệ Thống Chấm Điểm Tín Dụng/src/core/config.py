from __future__ import annotations

import os
from pathlib import Path
from dataclasses import dataclass

PROJECT_ROOT = Path(__file__).resolve().parents[2]


def _abs_path(value: str) -> Path:
    path = Path(value)
    if path.is_absolute():
        return path
    return PROJECT_ROOT / path


@dataclass(frozen=True)
class Settings:
    app_name: str = os.getenv("APP_NAME", "Credit Scoring System")
    app_env: str = os.getenv("APP_ENV", "development")
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///credit_scoring.db")
    data_path: Path = _abs_path(os.getenv("DATA_PATH", "data/credit_data.csv"))
    model_path: Path = _abs_path(os.getenv("MODEL_PATH", "models/credit_score_model.pkl"))
    metrics_path: Path = _abs_path(os.getenv("METRICS_PATH", "models/metrics.json"))
    min_credit_score: int = 300
    max_credit_score: int = 850


settings = Settings()


def ensure_directories() -> None:
    settings.data_path.parent.mkdir(parents=True, exist_ok=True)
    settings.model_path.parent.mkdir(parents=True, exist_ok=True)
    settings.metrics_path.parent.mkdir(parents=True, exist_ok=True)
