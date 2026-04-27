from __future__ import annotations

import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.ml.predictor import score_customer


if __name__ == "__main__":
    sample_path = PROJECT_ROOT / "samples" / "sample_customer.json"
    customer = json.loads(sample_path.read_text(encoding="utf-8"))
    result = score_customer(customer)
    print(json.dumps(result.model_dump(), ensure_ascii=False, indent=2))
