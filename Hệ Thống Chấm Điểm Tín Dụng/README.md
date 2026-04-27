# Hệ thống chấm điểm tín dụng bằng Python và Machine Learning

Đây là bản hoàn chỉnh ở mức đồ án/triển khai nội bộ nhỏ, không chỉ là demo form nhập liệu.

Hệ thống thực hiện đầy đủ luồng:

```text
Thu thập thông tin khách hàng
→ Xử lý dữ liệu theo pipeline
→ Gọi mô hình ML tính xác suất vỡ nợ
→ Quy đổi ra điểm tín dụng
→ Hiển thị kết quả kèm lý do chính
→ Lưu lịch sử và audit log
→ Cung cấp API để tích hợp hệ thống khác
```

---

## 1. Thành phần chính

| Thành phần | Mô tả |
|---|---|
| `app.py` | Giao diện web Streamlit để nhập khách hàng và xem kết quả |
| `api.py` | REST API bằng FastAPI |
| `src/ml/pipeline.py` | Pipeline ML hoàn chỉnh |
| `src/ml/feature_engineering.py` | Tạo biến tài chính: DTI, LTI, tỷ lệ trả góp/thu nhập... |
| `src/ml/training.py` | Train, đánh giá và lưu model |
| `src/ml/predictor.py` | Gọi model, tính xác suất vỡ nợ, quy đổi điểm |
| `src/ml/reasoner.py` | Sinh lý do chính ảnh hưởng đến kết quả |
| `src/db/` | Database SQLite, lưu lịch sử chấm điểm và audit log |
| `docs/` | Báo cáo, kịch bản thuyết trình, câu hỏi phản biện |
| `samples/` | Dữ liệu khách hàng mẫu |
| `tests/` | Test nhanh hệ thống |

---

## 2. Cài đặt trên Windows

### Cách khuyến nghị

Mở terminal trong thư mục project và chạy:

```powershell
python -m venv .venv
.\.venv\Scripts\activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python src/train.py
python -m streamlit run app.py
```

### Cách nhanh

Bấm file:

```text
setup_windows.bat
```

Sau đó chạy app:

```text
run_app_windows.bat
```

---

## 3. Chạy API

```powershell
python -m uvicorn api:app --reload --host 127.0.0.1 --port 8000
```

Mở tài liệu API:

```text
http://127.0.0.1:8000/docs
```

Endpoint chính:

| Method | URL | Mục đích |
|---|---|---|
| GET | `/health` | Kiểm tra hệ thống |
| POST | `/api/v1/score` | Chấm điểm khách hàng |
| GET | `/api/v1/applications` | Xem lịch sử chấm điểm |
| GET | `/api/v1/model/metrics` | Xem chỉ số mô hình |
| POST | `/api/v1/model/retrain` | Train lại mô hình |

---

## 4. Train mô hình

```powershell
python src/train.py
```

Sau khi train sẽ sinh:

```text
models/credit_score_model.pkl
models/metrics.json
data/credit_data.csv
```

---

## 5. Chấm điểm bằng CLI

```powershell
python src/predict.py
```

Hoặc:

```powershell
python src/cli.py score samples/sample_customer.json
```

---

## 6. Dữ liệu đầu vào

Hệ thống nhận các trường:

| Nhóm | Trường |
|---|---|
| Thông tin cá nhân | tuổi, số người phụ thuộc |
| Thu nhập | thu nhập hàng tháng, số năm làm việc, loại hình công việc |
| Khoản vay | số tiền vay, kỳ hạn vay, mục đích vay, tài sản đảm bảo |
| Tín dụng | lịch sử tín dụng, trả chậm, nợ hiện tại, số thẻ, tỷ lệ sử dụng hạn mức, số lần truy vấn tín dụng |

---

## 7. Pipeline xử lý dữ liệu

Pipeline gồm:

1. Feature engineering
2. Xử lý dữ liệu thiếu bằng median/mode
3. Chuẩn hóa biến số bằng StandardScaler
4. Mã hóa biến phân loại bằng OneHotEncoder
5. Mô hình Random Forest
6. Hiệu chỉnh xác suất bằng CalibratedClassifierCV

Các biến tài chính được tạo thêm:

| Biến | Ý nghĩa |
|---|---|
| `debt_to_income` | Tổng nợ / thu nhập năm |
| `loan_to_income` | Số tiền vay / thu nhập năm |
| `installment_to_income` | Trả góp ước tính / thu nhập tháng |
| `income_per_dependent` | Thu nhập chia theo số người phụ thuộc |
| `credit_history_age_ratio` | Lịch sử tín dụng so với tuổi |
| `has_collateral` | Có tài sản đảm bảo hay không |
| `late_payment_flag` | Có trả chậm hay không |
| `high_utilization_flag` | Có sử dụng hạn mức thẻ cao hay không |

---

## 8. Quy đổi điểm tín dụng

Mô hình dự đoán xác suất vỡ nợ `PD`. Sau đó quy đổi:

```text
credit_score = 850 - PD * 550
```

Thang điểm:

| Điểm | Hạng |
|---:|---|
| 800–850 | Xuất sắc |
| 740–799 | Rất tốt |
| 670–739 | Tốt |
| 580–669 | Trung bình |
| 300–579 | Rủi ro cao |

---

## 9. Lưu ý quan trọng

Hệ thống này phục vụ học tập, báo cáo và mô phỏng. Nếu dùng thực tế cần bổ sung:

- Dữ liệu thật đã được cho phép sử dụng.
- Kiểm định bias/fairness.
- Kiểm định pháp lý.
- Bảo mật dữ liệu cá nhân.
- Quy trình phê duyệt có người chịu trách nhiệm.
- Theo dõi drift của mô hình theo thời gian.
