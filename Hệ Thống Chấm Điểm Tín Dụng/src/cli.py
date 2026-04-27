from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.ml.predictor import score_customer
from src.ml.training import train_and_save


def main() -> None:
    parser = argparse.ArgumentParser(description="Credit Scoring System CLI")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("train", help="Train lại mô hình")

    score_parser = sub.add_parser("score", help="Chấm điểm một khách hàng từ file JSON")
    score_parser.add_argument("json_file", type=str, help="Đường dẫn file JSON chứa thông tin khách hàng")

    args = parser.parse_args()

    if args.command == "train":
        metrics = train_and_save()
        print(json.dumps(metrics, ensure_ascii=False, indent=2))
    elif args.command == "score":
        customer = json.loads(Path(args.json_file).read_text(encoding="utf-8"))
        result = score_customer(customer)
        print(json.dumps(result.model_dump(), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
