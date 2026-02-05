# 📊 Dataset Metadata: Media & Marketing Performance

## 1. Tổng quan (Overview)
Bộ dữ liệu **`media_all_channels.csv`** chứa thông tin chi tiết về hiệu suất của các chiến dịch Digital Marketing đa kênh. Dữ liệu này được sử dụng để phân tích ROI, so sánh hiệu quả các nền tảng quảng cáo và xây dựng mô hình dự báo doanh thu.

## 2. Thông số Kỹ thuật (Technical Specs)
* **Định dạng:** CSV.
* **Kích thước:** 7,644 dòng (rows), 15 cột (columns).
* **Chất lượng dữ liệu:** Dữ liệu sạch, không có giá trị khuyết (Non-Null).
* **Đặc tính:** Dữ liệu hỗn hợp giữa chuỗi thời gian (Time-series) và phân loại (Categorical).

## 3. Từ điển Dữ liệu (Data Dictionary)

### A. Thông tin Định danh & Phân loại (Categorical Variables)
* **`date`**: Ngày ghi nhận số liệu (Format: YYYY-MM-DD).
* **`channel`**: Kênh quảng cáo. Gồm 6 giá trị:
    * *Social Media:* Facebook, Instagram, LinkedIn, Twitter.
    * *Search/Display:* Google Ads.
    * *Owned Media:* Website.
* **`campaign`**: Loại chiến dịch Marketing. Gồm 7 giá trị đại diện cho các chiến thuật tâm lý khách hàng:
    * *Best Sellers, Flash Sale, New Arrivals, Must-Haves, Exclusive Offers, Limited Edition, Trending Now.*

### B. Biến Đầu vào - Nỗ lực (Input Metrics - Independent Variables)
* **`cost`**: Tổng chi phí quảng cáo đã chi tiêu.
* **`impressions`**: Số lượt hiển thị quảng cáo đến người dùng.
* **`clicks`**: Số lượt người dùng nhấp vào quảng cáo.

### C. Biến Đầu ra - Kết quả (Output Metrics - Target Variables)
* **`conversions`**: Số lượng hành động chuyển đổi thành công (đơn hàng/đăng ký).
* **`revenue`**: Tổng doanh thu mang lại (Biến mục tiêu chính cho mô hình Hồi quy).

### D. Chỉ số Phái sinh/KPIs (Derived Metrics)
*(Lưu ý: Các biến này được tính toán trực tiếp từ Cost và Revenue. Cần loại bỏ khi chạy mô hình dự báo Revenue để tránh lỗi Data Leakage)*
* **`ctr`** (Click-Through Rate): Tỷ lệ nhấp (`clicks` / `impressions`).
* **`cpc`** (Cost Per Click): Chi phí trung bình mỗi lượt nhấp.
* **`cpa`** (Cost Per Acquisition): Chi phí trung bình mỗi chuyển đổi.
* **`conversion_rate`**: Tỷ lệ chuyển đổi (`conversions` / `clicks`).
* **`roas`** (Return On Ad Spend): Lợi tức trên chi tiêu quảng cáo (`revenue` / `cost`).
* **`roi`** (Return On Investment): Lợi nhuận ròng trên chi phí đầu tư.
* **`profit_margin`**: Biên lợi nhuận.

## 4. Gợi ý Hướng Phân tích (Analysis Objectives)
1.  **Thống kê mô tả (Descriptive):** So sánh ROAS giữa các kênh, xu hướng doanh thu theo thời gian.
2.  **Mô hình hóa (Predictive):** Xây dựng mô hình **Đa hồi quy tuyến tính (Multiple Linear Regression)** để dự báo `revenue` dựa trên `cost`, `impressions` và các biến giả của `channel`/`campaign`.