# 📊 Phân Tích Hiệu Quả Digital Marketing Đa Kênh

## 📝 Tổng Quan (Overview)
Dự án này là một ứng dụng web (Dashboard) được xây dựng bằng **Python** và **Streamlit** để phân tích hiệu suất của các chiến dịch Digital Marketing trên nhiều nền tảng khác nhau (Social Media, Search, Website).

Mục tiêu chính:
1.  **Trực quan hóa dữ liệu:** Cung cấp cái nhìn tổng quan về doanh thu, chi phí, và hiệu quả (ROI/ROAS) của từng kênh và chiến dịch.
2.  **Xử lý dữ liệu:** Chuẩn bị và làm sạch dữ liệu để phục vụ cho các mô hình dự báo (Hồi quy tuyến tính).

## 🚀 Tính Năng Chính (Features)
*   **Dashboard Tương tác:**
    *   **Bộ lọc đa chiều:** Lọc dữ liệu theo Khoảng thời gian, Kênh Marketing (Social, Search, Website), và Loại Chiến dịch.
    *   **KPI Cards:** Theo dõi nhanh các chỉ số quan trọng: Tổng doanh thu, Chi phí, Lợi nhuận, Số chuyển đổi, và ROAS trung bình.
*   **Biểu đồ Trực quan:**
    *   **Marketing Funnel:** Biểu đồ phễu thể hiện tỷ lệ chuyển đổi từ Impressions → Clicks → Conversions.
    *   **Time-series Analysis:** Biểu đồ xu hướng Revenue và Cost theo thời gian với 2 trục đo.
    *   **Comparative Analysis:** So sánh hiệu quả Revenue giữa các Kênh và các Chiến dịch.
    *   **ROI Analysis:** Biểu đồ phân tán (Scatter plot) đánh giá mối tương quan giữa Chi phí và Doanh thu.
*   **Data Processing (Chương 3):**
    *   Tự động làm sạch dữ liệu (loại bỏ giá trị null, các cột phái sinh thừa).
    *   Mã hóa biến phân loại (One-Hot Encoding) cho 'Channel' và 'Campaign'.
    *   Xuất dữ liệu sạch (CSV) để chạy mô hình Machine Learning.

## 📂 Cấu Trúc Dự Án
```
ptdl/
├── scr/
│   └── app.py              # Mã nguồn chính của ứng dụng Streamlit (Dashboard)
├── media_all_channels.csv  # Bộ dữ liệu gốc (Marketing Performance)
├── docs.md                 # Tài liệu đặc tả dữ liệu chi tiết
├── de_cuong.md             # Đề cương chi tiết của dự án
├── requirements.txt        # Danh sách các thư viện Python cần thiết
└── README.md               # Tài liệu hướng dẫn sử dụng (File này)
```

## 🛠️ Hướng Dẫn Cài Đặt & Chạy

### 1. Cài đặt môi trường
Đảm bảo bạn đã cài đặt Python. Sau đó cài đặt các thư viện cần thiết:
```bash
pip install -r requirements.txt
```

*Các thư viện chính:* `streamlit`, `pandas`, `plotly`, `seaborn`, `matplotlib`.

### 2. Chạy ứng dụng
Mở terminal tại thư mục gốc của dự án và chạy lệnh:
```bash
streamlit run scr/app.py
```
Ứng dụng sẽ tự động mở trên trình duyệt tại địa chỉ: `http://localhost:8501`

## 📊 Thông Tin Dữ Liệu
Bộ dữ liệu `media_all_channels.csv` giả lập hiệu quả quảng cáo với các trường thông tin chính:
*   **Thời gian:** `date`
*   **Kích thước (Dimensions):** `channel` (6 kênh), `campaign` (7 loại chiến dịch).
*   **Số liệu (Metrics):** `cost` (Chi phí), `impressions` (Lượt hiển thị), `clicks` (Lượt nhấp), `conversions` (Chuyển đổi), `revenue` (Doanh thu).

---
*Dự án phục vụ môn học Phân tích Dữ liệu lớn.*
