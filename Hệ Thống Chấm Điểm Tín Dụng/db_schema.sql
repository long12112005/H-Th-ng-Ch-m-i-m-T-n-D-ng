-- SQLite schema được SQLAlchemy tự tạo khi chạy hệ thống.
-- File này dùng để báo cáo cấu trúc dữ liệu chính.

CREATE TABLE score_applications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created_at DATETIME,
    customer_name VARCHAR(120),
    age INTEGER,
    monthly_income FLOAT,
    loan_amount FLOAT,
    loan_term_months INTEGER,
    credit_history_years FLOAT,
    late_payments_12m INTEGER,
    existing_debt FLOAT,
    num_credit_cards INTEGER,
    credit_utilization FLOAT,
    employment_years FLOAT,
    employment_type VARCHAR(40),
    home_ownership VARCHAR(40),
    loan_purpose VARCHAR(40),
    collateral_type VARCHAR(40),
    number_of_dependents INTEGER,
    recent_credit_inquiries INTEGER,
    probability_default FLOAT,
    credit_score INTEGER,
    rating VARCHAR(40),
    decision VARCHAR(80),
    risk_level VARCHAR(40),
    engineered_features JSON,
    main_reasons JSON,
    recommendation TEXT
);

CREATE TABLE audit_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created_at DATETIME,
    action VARCHAR(80),
    detail TEXT
);
