from __future__ import annotations

import json
import pandas as pd
import streamlit as st

from src.core.schemas import CustomerInput
from src.ml.predictor import score_customer
from src.ml.training import load_metrics, train_and_save
from src.db.database import init_db, SessionLocal
from src.db.repository import save_score_application, list_applications, list_audit_logs

st.set_page_config(
    page_title="Hệ thống chấm điểm tín dụng",
    page_icon="💳",
    layout="wide",
)

init_db()


page = st.sidebar.radio(
    "Chức năng",
    ["🧮 Chấm điểm khách hàng", "📊 Lịch sử chấm điểm", "🤖 Thông tin mô hình", "🧾 Nhật ký hệ thống", ""],
)


def vnd(value: float) -> str:
    return f"{value:,.0f} VND".replace(",", ".")


if page == "🧮 Chấm điểm khách hàng":
    st.subheader("1. Thu thập thông tin khách hàng")

    with st.form("score_form"):
        col1, col2, col3 = st.columns(3)

        with col1:
            full_name = st.text_input("Họ tên khách hàng", "Nguyễn Văn A")
            age = st.number_input("Tuổi", min_value=18, max_value=80, value=30)
            monthly_income = st.number_input("Thu nhập hàng tháng", min_value=1_000_000, value=20_000_000, step=1_000_000)
            employment_years = st.number_input("Số năm làm việc", min_value=0.0, max_value=60.0, value=3.0, step=0.5)
            employment_type = st.selectbox("Loại hình công việc", ["full_time", "part_time", "self_employed", "contract", "unemployed"])

        with col2:
            loan_amount = st.number_input("Số tiền vay", min_value=1_000_000, value=100_000_000, step=5_000_000)
            loan_term_months = st.selectbox("Kỳ hạn vay", [6, 12, 18, 24, 36, 48, 60, 84, 120], index=3)
            loan_purpose = st.selectbox("Mục đích vay", ["personal", "business", "education", "home", "vehicle", "medical", "debt_consolidation"])
            collateral_type = st.selectbox("Tài sản đảm bảo", ["none", "vehicle", "real_estate", "savings", "guarantor"])
            home_ownership = st.selectbox("Nhà ở", ["rent", "own", "mortgage", "family"])

        with col3:
            credit_history_years = st.number_input("Số năm lịch sử tín dụng", min_value=0.0, max_value=60.0, value=4.0, step=0.5)
            late_payments_12m = st.number_input("Số lần trả chậm 12 tháng", min_value=0, max_value=24, value=0)
            existing_debt = st.number_input("Tổng nợ hiện tại", min_value=0, value=20_000_000, step=5_000_000)
            num_credit_cards = st.number_input("Số thẻ tín dụng", min_value=0, max_value=20, value=2)
            credit_utilization = st.slider("Tỷ lệ sử dụng hạn mức thẻ", min_value=0.0, max_value=1.0, value=0.35, step=0.01)
            number_of_dependents = st.number_input("Số người phụ thuộc", min_value=0, max_value=15, value=1)
            recent_credit_inquiries = st.number_input("Số lần truy vấn tín dụng gần đây", min_value=0, max_value=20, value=1)

        submitted = st.form_submit_button("🚀 Chấm điểm tín dụng", use_container_width=True)

    if submitted:
        customer = CustomerInput(
            full_name=full_name,
            age=age,
            monthly_income=monthly_income,
            loan_amount=loan_amount,
            loan_term_months=loan_term_months,
            credit_history_years=credit_history_years,
            late_payments_12m=late_payments_12m,
            existing_debt=existing_debt,
            num_credit_cards=num_credit_cards,
            credit_utilization=credit_utilization,
            employment_years=employment_years,
            employment_type=employment_type,
            home_ownership=home_ownership,
            loan_purpose=loan_purpose,
            collateral_type=collateral_type,
            number_of_dependents=number_of_dependents,
            recent_credit_inquiries=recent_credit_inquiries,
        )

        result = score_customer(customer)
        with SessionLocal() as session:
            save_score_application(session, customer, result)

        st.subheader("2. Kết quả chấm điểm")
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Điểm tín dụng", result.credit_score)
        m2.metric("Xác suất vỡ nợ", f"{result.probability_default:.2%}")
        m3.metric("Xếp hạng", result.rating)
        m4.metric("Mức rủi ro", result.risk_level)

        if result.decision == "Đề xuất phê duyệt":
            st.success(f"✅ {result.decision}")
        elif result.decision == "Cần thẩm định thêm":
            st.warning(f"⚠️ {result.decision}")
        else:
            st.error(f"⛔ {result.decision}")

        st.info(result.recommendation)

        st.subheader("3. Lý do chính ảnh hưởng đến kết quả")
        for reason in result.main_reasons:
            icon = "🔴" if reason.impact == "risk_increase" else "🟢" if reason.impact == "risk_decrease" else "⚪"
            st.write(f"{icon} **{reason.factor}** — {reason.message}")

        st.subheader("4. Biến tài chính sau pipeline")
        features = pd.DataFrame([result.engineered_features]).T.reset_index()
        features.columns = ["Biến", "Giá trị"]
        st.dataframe(features, use_container_width=True)

        with st.expander("Xem JSON kết quả"):
            st.json(result.model_dump())

elif page == "📊 Lịch sử chấm điểm":
    st.subheader("Lịch sử chấm điểm khách hàng")
    with SessionLocal() as session:
        rows = list_applications(session, limit=200)
    if not rows:
        st.info("Chưa có dữ liệu chấm điểm.")
    else:
        df = pd.DataFrame([
            {
                "Thời gian": r.created_at,
                "Khách hàng": r.customer_name,
                "Điểm": r.credit_score,
                "PD": r.probability_default,
                "Hạng": r.rating,
                "Rủi ro": r.risk_level,
                "Quyết định": r.decision,
                "Số tiền vay": r.loan_amount,
                "Thu nhập tháng": r.monthly_income,
            }
            for r in rows
        ])
        st.dataframe(df, use_container_width=True)
        st.download_button(
            "⬇️ Tải lịch sử CSV",
            df.to_csv(index=False).encode("utf-8-sig"),
            file_name="lich_su_cham_diem.csv",
            mime="text/csv",
        )

elif page == "🤖 Thông tin mô hình":
    st.subheader("Thông tin mô hình Machine Learning")
    metrics = load_metrics()
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("🔁 Train lại mô hình", use_container_width=True):
            with st.spinner("Đang train lại mô hình..."):
                metrics = train_and_save()
            st.success("Train lại mô hình thành công.")
    with col2:
        st.write("Mô hình: **Random Forest + Probability Calibration**")
        st.write("Pipeline: **Feature Engineering + Impute + Scale + One-hot + ML Model**")

    if metrics:
        c1, c2, c3, c4, c5 = st.columns(5)
        c1.metric("ROC AUC", metrics.get("roc_auc"))
        c2.metric("Accuracy", metrics.get("accuracy"))
        c3.metric("Precision", metrics.get("precision"))
        c4.metric("Recall", metrics.get("recall"))
        c5.metric("F1", metrics.get("f1"))
        st.json(metrics)
    else:
        st.warning("Chưa có metrics. Hãy train mô hình trước.")

elif page == "🧾 Nhật ký hệ thống":
    st.subheader("Audit log")
    with SessionLocal() as session:
        logs = list_audit_logs(session, limit=200)
    if logs:
        df = pd.DataFrame([{"Thời gian": x.created_at, "Hành động": x.action, "Chi tiết": x.detail} for x in logs])
        st.dataframe(df, use_container_width=True)
    else:
        st.info("Chưa có log.")


    
