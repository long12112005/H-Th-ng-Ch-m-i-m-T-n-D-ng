from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.ml.training import train_and_save
from src.core.config import settings


if __name__ == "__main__":
    print("Đang train mô hình chấm điểm tín dụng...")
    metrics = train_and_save()
    print("\n===== TRAIN XONG =====")
    print(f"Model: {settings.model_path}")
    print(f"Metrics: {settings.metrics_path}")
    print(f"ROC AUC: {metrics['roc_auc']}")
    print(f"Accuracy: {metrics['accuracy']}")
    print(f"Precision: {metrics['precision']}")
    print(f"Recall: {metrics['recall']}")
    print(f"F1: {metrics['f1']}")
