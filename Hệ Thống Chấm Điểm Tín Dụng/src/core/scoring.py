from __future__ import annotations


def probability_to_credit_score(probability_default: float, min_score: int = 300, max_score: int = 850) -> int:
    """Quy đổi xác suất vỡ nợ thành điểm tín dụng.

    probability_default càng cao thì điểm càng thấp.
    Công thức dùng min/max để dễ giải thích khi báo cáo.
    """
    p = max(0.0, min(1.0, float(probability_default)))
    score = max_score - p * (max_score - min_score)
    return int(round(score))


def get_credit_rating(score: int) -> str:
    if score >= 800:
        return "Xuất sắc"
    if score >= 740:
        return "Rất tốt"
    if score >= 670:
        return "Tốt"
    if score >= 580:
        return "Trung bình"
    return "Rủi ro cao"


def get_risk_level(probability_default: float) -> str:
    if probability_default < 0.15:
        return "Thấp"
    if probability_default < 0.35:
        return "Trung bình"
    if probability_default < 0.60:
        return "Cao"
    return "Rất cao"


def get_decision(score: int, probability_default: float) -> str:
    if score >= 700 and probability_default < 0.30:
        return "Đề xuất phê duyệt"
    if score >= 580 and probability_default < 0.55:
        return "Cần thẩm định thêm"
    return "Đề xuất từ chối"


def get_recommendation(score: int, probability_default: float) -> str:
    if score >= 700 and probability_default < 0.30:
        return "Khách hàng có hồ sơ tương đối tốt. Có thể phê duyệt nếu giấy tờ thu nhập và thông tin khoản vay hợp lệ."
    if score >= 580:
        return "Nên yêu cầu bổ sung hồ sơ, giảm số tiền vay, tăng tài sản đảm bảo hoặc kiểm tra lại lịch sử trả nợ."
    return "Rủi ro cao. Nên từ chối hoặc chỉ xem xét khi có tài sản đảm bảo mạnh và phương án trả nợ rõ ràng."
