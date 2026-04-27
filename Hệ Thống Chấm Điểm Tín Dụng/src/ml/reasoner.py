from __future__ import annotations

from src.core.schemas import Reason


def build_reasons(customer: dict, engineered: dict) -> list[Reason]:
    reasons: list[Reason] = []

    dti = engineered.get("debt_to_income", 0)
    lti = engineered.get("loan_to_income", 0)
    installment = engineered.get("installment_to_income", 0)
    credit_history = float(customer.get("credit_history_years", 0))
    late = int(customer.get("late_payments_12m", 0))
    utilization = float(customer.get("credit_utilization", 0))
    employment_years = float(customer.get("employment_years", 0))
    inquiries = int(customer.get("recent_credit_inquiries", 0))
    collateral = customer.get("collateral_type", "none")

    if late >= 3:
        reasons.append(Reason(factor="Lịch sử trả chậm", impact="risk_increase", severity="high", message=f"Có {late} lần trả chậm trong 12 tháng gần nhất."))
    elif late >= 1:
        reasons.append(Reason(factor="Lịch sử trả chậm", impact="risk_increase", severity="medium", message=f"Có {late} lần trả chậm trong 12 tháng gần nhất."))
    else:
        reasons.append(Reason(factor="Lịch sử trả nợ", impact="risk_decrease", severity="low", message="Không ghi nhận trả chậm trong 12 tháng gần nhất."))

    if dti >= 0.55:
        reasons.append(Reason(factor="Tỷ lệ nợ / thu nhập", impact="risk_increase", severity="high", message=f"Tỷ lệ nợ trên thu nhập khoảng {dti:.0%}, cao so với ngưỡng an toàn."))
    elif dti >= 0.35:
        reasons.append(Reason(factor="Tỷ lệ nợ / thu nhập", impact="risk_increase", severity="medium", message=f"Tỷ lệ nợ trên thu nhập khoảng {dti:.0%}, cần thẩm định kỹ."))
    else:
        reasons.append(Reason(factor="Tỷ lệ nợ / thu nhập", impact="risk_decrease", severity="low", message=f"Tỷ lệ nợ trên thu nhập khoảng {dti:.0%}, tương đối kiểm soát được."))

    if installment >= 0.5:
        reasons.append(Reason(factor="Gánh nặng trả góp", impact="risk_increase", severity="high", message=f"Khoản trả góp ước tính chiếm khoảng {installment:.0%} thu nhập tháng."))
    elif installment >= 0.3:
        reasons.append(Reason(factor="Gánh nặng trả góp", impact="risk_increase", severity="medium", message=f"Khoản trả góp ước tính chiếm khoảng {installment:.0%} thu nhập tháng."))

    if lti >= 3:
        reasons.append(Reason(factor="Khoản vay so với thu nhập", impact="risk_increase", severity="high", message=f"Số tiền vay bằng khoảng {lti:.1f} lần thu nhập năm."))
    elif lti >= 1.5:
        reasons.append(Reason(factor="Khoản vay so với thu nhập", impact="risk_increase", severity="medium", message=f"Số tiền vay bằng khoảng {lti:.1f} lần thu nhập năm."))

    if credit_history < 1:
        reasons.append(Reason(factor="Lịch sử tín dụng", impact="risk_increase", severity="medium", message="Lịch sử tín dụng còn rất ngắn, dữ liệu đánh giá hạn chế."))
    elif credit_history >= 5:
        reasons.append(Reason(factor="Lịch sử tín dụng", impact="risk_decrease", severity="low", message="Có lịch sử tín dụng đủ dài để tham chiếu."))

    if utilization >= 0.8:
        reasons.append(Reason(factor="Sử dụng hạn mức thẻ", impact="risk_increase", severity="high", message=f"Tỷ lệ sử dụng hạn mức thẻ khoảng {utilization:.0%}, rất cao."))
    elif utilization >= 0.6:
        reasons.append(Reason(factor="Sử dụng hạn mức thẻ", impact="risk_increase", severity="medium", message=f"Tỷ lệ sử dụng hạn mức thẻ khoảng {utilization:.0%}, cần theo dõi."))

    if employment_years < 1:
        reasons.append(Reason(factor="Thâm niên công việc", impact="risk_increase", severity="medium", message="Thâm niên công việc dưới 1 năm, thu nhập có thể chưa ổn định."))
    elif employment_years >= 3:
        reasons.append(Reason(factor="Thâm niên công việc", impact="risk_decrease", severity="low", message="Thâm niên công việc tương đối ổn định."))

    if inquiries >= 5:
        reasons.append(Reason(factor="Truy vấn tín dụng gần đây", impact="risk_increase", severity="medium", message=f"Có {inquiries} lần truy vấn tín dụng gần đây, có thể đang vay nhiều nơi."))

    if collateral != "none":
        reasons.append(Reason(factor="Tài sản đảm bảo", impact="risk_decrease", severity="low", message="Khoản vay có tài sản đảm bảo hoặc người bảo lãnh."))
    else:
        reasons.append(Reason(factor="Tài sản đảm bảo", impact="neutral", severity="low", message="Không có tài sản đảm bảo, cần dựa nhiều hơn vào dòng tiền trả nợ."))

    severity_order = {"high": 3, "medium": 2, "low": 1}
    impact_order = {"risk_increase": 2, "neutral": 1, "risk_decrease": 0}
    reasons.sort(key=lambda r: (impact_order[r.impact], severity_order[r.severity]), reverse=True)
    return reasons[:5]
