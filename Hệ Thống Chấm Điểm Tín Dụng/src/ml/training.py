from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

import joblib
import pandas as pd
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, roc_auc_score, precision_score, recall_score, f1_score
from sklearn.model_selection import train_test_split

from src.core.config import settings, ensure_directories
from src.ml.data_generator import ensure_dataset
from src.ml.pipeline import build_model_pipeline

TARGET = "default"
DROP_COLUMNS = ["full_name"]


def train_and_save(data_path: Path | None = None, model_path: Path | None = None, metrics_path: Path | None = None) -> dict:
    ensure_directories()
    data_path = data_path or settings.data_path
    model_path = model_path or settings.model_path
    metrics_path = metrics_path or settings.metrics_path

    df = ensure_dataset(data_path)
    if TARGET not in df.columns:
        raise ValueError(f"Dataset phải có cột target '{TARGET}'.")

    X = df.drop(columns=[TARGET] + [c for c in DROP_COLUMNS if c in df.columns])
    y = df[TARGET].astype(int)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    pipeline = build_model_pipeline()
    pipeline.fit(X_train, y_train)

    y_pred = pipeline.predict(X_test)
    y_proba = pipeline.predict_proba(X_test)[:, 1]

    metrics = {
        "trained_at": datetime.now().isoformat(timespec="seconds"),
        "rows": int(len(df)),
        "features": list(X.columns),
        "target_rate_default": round(float(y.mean()), 4),
        "accuracy": round(float(accuracy_score(y_test, y_pred)), 4),
        "roc_auc": round(float(roc_auc_score(y_test, y_proba)), 4),
        "precision": round(float(precision_score(y_test, y_pred, zero_division=0)), 4),
        "recall": round(float(recall_score(y_test, y_pred, zero_division=0)), 4),
        "f1": round(float(f1_score(y_test, y_pred, zero_division=0)), 4),
        "confusion_matrix": confusion_matrix(y_test, y_pred).tolist(),
        "classification_report": classification_report(y_test, y_pred, output_dict=True, zero_division=0),
    }

    model_path.parent.mkdir(parents=True, exist_ok=True)
    metrics_path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(pipeline, model_path)
    metrics_path.write_text(json.dumps(metrics, ensure_ascii=False, indent=2), encoding="utf-8")
    return metrics


def load_metrics(metrics_path: Path | None = None) -> dict:
    metrics_path = metrics_path or settings.metrics_path
    if not metrics_path.exists():
        return {}
    return json.loads(metrics_path.read_text(encoding="utf-8"))
