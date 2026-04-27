import json
from pathlib import Path

from src.core.schemas import CustomerInput
from src.ml.predictor import score_customer


def test_score_customer_smoke():
    data = json.loads(Path("samples/sample_customer.json").read_text(encoding="utf-8"))
    customer = CustomerInput(**data)
    result = score_customer(customer)
    assert 300 <= result.credit_score <= 850
    assert 0 <= result.probability_default <= 1
    assert len(result.main_reasons) > 0
