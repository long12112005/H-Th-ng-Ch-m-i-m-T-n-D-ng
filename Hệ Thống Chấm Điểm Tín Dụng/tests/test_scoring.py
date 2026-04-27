from src.core.scoring import probability_to_credit_score, get_credit_rating, get_decision


def test_probability_to_credit_score_bounds():
    assert probability_to_credit_score(0) == 850
    assert probability_to_credit_score(1) == 300
    assert 300 <= probability_to_credit_score(0.5) <= 850


def test_rating():
    assert get_credit_rating(820) == "Xuất sắc"
    assert get_credit_rating(760) == "Rất tốt"
    assert get_credit_rating(700) == "Tốt"
    assert get_credit_rating(600) == "Trung bình"
    assert get_credit_rating(500) == "Rủi ro cao"


def test_decision():
    assert get_decision(720, 0.2) == "Đề xuất phê duyệt"
    assert get_decision(620, 0.4) == "Cần thẩm định thêm"
    assert get_decision(500, 0.7) == "Đề xuất từ chối"
